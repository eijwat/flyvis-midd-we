#!/usr/bin/env python3
"""Store decoded flow fields for the static MIDD stimuli (official 50 models).

The original release kept only scalar summaries of the MIDD responses, so the
vector fields in Fig. 1 could not be redrawn. This script reruns the same
single-BoxEye protocol (FlyVis 1.2.0, 1-s fade-in on frame 0, 50 frames at
50 Hz, CPU float32, eval mode) and saves, for every model and condition,
the decoder output averaged over analysis frames 10-49 and the frame-25
snapshot. It also recomputes the mean signed tangential flow T and checks it
against the stored table ``data/precomputed/fig01/fig1_tangent_per_model_condition.csv``.

Usage (FLYVIS_ROOT_DIR must point at the downloaded pretrained models):

    CUDA_VISIBLE_DEVICES="" FLYVIS_ROOT_DIR=~/flyvis_data python scripts/generate_fig1_flow_fields.py
"""
from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import flyvis  # noqa: E402
from flyvis.datasets.rendering import BoxEye  # noqa: E402

from flyvis_midd.flow import run_flow_inference  # noqa: E402
from flyvis_midd.rotation import image_rotation_flow_metrics  # noqa: E402
from flyvis_midd.stimuli import (  # noqa: E402
    build_3midd_sequences,
    build_4midd_sequences,
    render_sector_image,
)

N_FRAMES, DT, FADE = 50, 1 / 50, 1.0
START, STOP, SNAPSHOT = 10, 50, 25
GROUPS = (
    ("3MIDD_048", build_3midd_sequences(48)),
    ("3MIDD_207", build_3midd_sequences(207)),
    ("4MIDD_085_170", build_4midd_sequences(85, 170)),
)
VARIANTS = ("original", "mirror", "negative")
OUT = ROOT / "data/precomputed/fig01/fig1_flow_fields.npz"


def main(model_numbers=range(50)):
    torch.set_num_threads(8)
    eye = BoxEye(extent=15, kernel_size=13)
    conditions, images = [], []
    for group, variants in GROUPS:
        for variant in VARIANTS:
            image, _ = render_sector_image(variants[variant])
            conditions.append(f"{group}__{variant}")
            images.append(image)
    images = np.stack(images)
    movies = np.repeat(images[:, None].astype(np.float32) / 255.0, N_FRAMES, axis=1)
    rendered = eye(torch.as_tensor(movies))  # (condition, frame, 1, 721)
    centers = np.asarray(eye.receptor_centers, float)  # (721, 2) as (y, x)

    model_ids = [f"flow/0000/{i:03d}" for i in model_numbers]
    mean_flow = np.zeros((len(model_ids), len(conditions), 2, rendered.shape[-1]), np.float32)
    snap_flow = np.zeros_like(mean_flow)
    rows = []
    for m, model_id in enumerate(model_ids):
        view = flyvis.NetworkView(flyvis.results_dir / model_id)
        network = view.init_network()
        decoder = view.init_decoder()["flow"]
        flow = run_flow_inference(rendered, network, decoder, dt=DT, fade=FADE)["flow"].numpy()
        # flow: (condition, frame, 2, receptor), raw decoder (u, v)
        mean_flow[m] = flow[:, START:STOP].mean(1)
        snap_flow[m] = flow[:, SNAPSHOT]
        for c, condition in enumerate(conditions):
            group, variant = condition.split("__")
            metrics = image_rotation_flow_metrics(
                centers, np.moveaxis(flow[c, START:STOP], 1, -1)
            )
            rows.append({
                "model_id": model_id, "group": group, "variant": variant,
                "mean_signed_tangent": metrics["mean_signed_tangent"],
                "mean_flow_magnitude": metrics["mean_flow_magnitude"],
            })
        print(model_id, "done", flush=True)

    np.savez_compressed(
        OUT,
        mean_flow_uv=mean_flow, snapshot_flow_uv=snap_flow,
        model_ids=np.array(model_ids), conditions=np.array(conditions),
        receptor_centers_yx=centers.astype(np.float32),
        rendered_luminance=rendered[:, 0, 0].numpy().astype(np.float32),
        source_images=images,
    )
    new = pd.DataFrame(rows)
    new.to_csv(OUT.with_name("fig1_flow_fields_tangent_check.csv"), index=False)
    old = pd.read_csv(ROOT / "data/precomputed/fig01/fig1_tangent_per_model_condition.csv")
    merged = new.merge(old, on=["model_id", "group", "variant"], suffixes=("_new", "_stored"))
    diff = (merged.mean_signed_tangent_new - merged.mean_signed_tangent_stored).abs()
    summary = {
        "flyvis_version": flyvis.__version__, "torch_version": torch.__version__,
        "n_models": len(model_ids), "conditions": conditions,
        "frames_mean": [START, STOP], "frame_snapshot": SNAPSHOT,
        "compared_rows": int(len(merged)),
        "max_abs_T_difference_vs_stored": float(diff.max()),
        "max_abs_stored_T": float(merged.mean_signed_tangent_stored.abs().max()),
    }
    OUT.with_name("fig1_flow_fields_metadata.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    numbers = [int(a) for a in sys.argv[1:]] or range(50)
    main(numbers)
