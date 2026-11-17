#!/usr/bin/env python3
"""Draw decoded flow for a moving propeller and for static MIDD patterns.

Reads stored fields only (no FlyVis needed):
  data/precomputed/fig01/fig1_flow_fields.npz            (static MIDD, 50 models)
  data/precomputed/supplementary/figS1/propeller_*       (physical rotation)

Rows: physically rotating propeller (sign calibration), 3MIDD C=48, 3MIDD C=207.
For the static patterns the Original/Mirror half-difference field is drawn; its mean
tangential component is exactly the antisymmetric scalar A of the manuscript.
Everything is drawn in image coordinates (x rightward, y downward), so a
clockwise arrow on the page is clockwise on the screen that showed the
stimulus. Decoder v is negated once, as in the analysis code.

Usage: python scripts/draw_fig1_flow.py [ensemble|<model number>]
"""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
CW_COLOR, CCW_COLOR = "#c2410c", "#1d4ed8"  # warm = clockwise, cool = counterclockwise
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "ccw_cw", [CCW_COLOR, "#93b4f0", "#f1f1ee", "#f0a880", CW_COLOR])


def tangential(centers, uv_image):
    cy, cx = centers.mean(0)
    dy, dx = centers[:, 0] - cy, centers[:, 1] - cx
    r = np.hypot(dx, dy)
    rr = np.maximum(r, 1e-9)
    t = uv_image[0] * (-dy / rr) + uv_image[1] * (dx / rr)
    mask = (r >= 0.14 * r.max()) & (r <= 0.98 * r.max())
    return t, mask, r.max()


def rotation_arrow(ax, clockwise, radius, color):
    """Curved arrow outside the field showing the net direction."""
    a0, a1 = (-150, -30) if clockwise else (-30, -150)  # image coords, y down
    p0 = radius * np.array([np.cos(np.deg2rad(a0)), np.sin(np.deg2rad(a0))])
    p1 = radius * np.array([np.cos(np.deg2rad(a1)), np.sin(np.deg2rad(a1))])
    rad = -0.45 if clockwise else 0.45
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}",
                                 arrowstyle="-|>", mutation_scale=22, lw=2.6,
                                 color=color, clip_on=False, zorder=5))


def hexmap(ax, centers, values, mask, vmax):
    ax.scatter(centers[~mask, 1], centers[~mask, 0], c="#e9e9e6", s=HEX, marker="h", linewidths=0)
    ax.scatter(centers[mask, 1], centers[mask, 0], c=values[mask], cmap=CMAP,
               norm=TwoSlopeNorm(0, -vmax, vmax), s=HEX, marker="h", linewidths=0)


def arrows(ax, centers, uv, lum=None):
    if lum is not None:
        ax.scatter(centers[:, 1], centers[:, 0], c=lum, cmap="gray", vmin=0, vmax=1,
                   s=HEX, marker="h", linewidths=0, alpha=0.45)
    speed = np.hypot(uv[0], uv[1])
    scale = np.percentile(speed, 95) / 24.0   # 95th-percentile arrow is ~24 px long
    ax.quiver(centers[:, 1], centers[:, 0], uv[0], uv[1], angles="xy", scale_units="xy",
              scale=scale, width=0.0066, headwidth=4.0, headlength=4.4, color="#e11d1d",
              zorder=3)


HEX, LIM = 74, 215


def main(which="ensemble"):
    z = np.load(ROOT / "data/precomputed/fig01/fig1_flow_fields.npz")
    conditions = list(z["conditions"])
    centers = z["receptor_centers_yx"].astype(float)
    centers = centers - centers.mean(0)
    base = ROOT / "data/precomputed/supplementary/figS1"
    prop = np.load(base / "propeller_flow_50models.npy", mmap_mode="r")
    pr = np.load(base / "propeller_boxeye_rendered.npz")
    ps = np.load(base / "propeller_sequences.npz")
    names = [str(n) for n in pr["names"]]
    i_cw = [i for i, n in enumerate(names) if n.upper().startswith("CW")][0]
    pick = slice(None) if which == "ensemble" else [int(which)]
    label = "mean of 50 models" if which == "ensemble" else f"model {int(which):03d}"
    midd = z["mean_flow_uv"][pick].astype(float).mean(0)             # (condition, 2, receptor)
    pflow = np.asarray(prop[pick, i_cw, 10:50], float).mean((0, 1))  # (2, receptor)

    def image_uv(flow):          # decoder (u, v) -> image coordinates, y downward
        return np.stack([flow[0], -flow[1]])

    rows = [("Moving propeller\n(physically clockwise)", ps["frames"][i_cw, 25], None,
             image_uv(pflow), pr["luminance"][i_cw, 25, 0], "Decoded flow")]
    for group, title in (("3MIDD_048", "Static 3MIDD\nC = 48 (dark gray)"),
                         ("3MIDD_207", "Static 3MIDD\nC = 207 (light gray)")):
        o, m = conditions.index(group + "__original"), conditions.index(group + "__mirror")
        rows.append((title, z["source_images"][o], z["source_images"][m],
                     image_uv((midd[o] - midd[m]) / 2), None,
                     "Decoded flow for Original\n(component that reverses in Mirror)"))

    plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(3, 4, figsize=(13.2, 11.8),
                             gridspec_kw={"hspace": 0.34, "wspace": 0.05})
    for i, (title, img_a, img_b, uv, lum, flow_title) in enumerate(rows):
        t, mask, rmax = tangential(centers, uv)
        mean_t = t[mask].mean()
        clockwise = mean_t > 0
        color = CW_COLOR if clockwise else CCW_COLOR
        ext = (-LIM * 0.91, LIM * 0.91, LIM * 0.91, -LIM * 0.91)
        axes[i, 0].imshow(img_a, cmap="gray", vmin=0, vmax=1 if img_a.max() <= 1 else 255,
                          extent=ext, interpolation="lanczos")
        axes[i, 0].set_title("Stimulus" if img_b is None else "Original", fontsize=11, pad=16)
        if img_b is not None:
            axes[i, 1].imshow(img_b, cmap="gray", vmin=0, vmax=255, extent=ext,
                              interpolation="lanczos")
            axes[i, 1].set_title("Mirror", fontsize=11, pad=16)
            # the half-difference field describes Original; Mirror has the opposite sign
            rotation_arrow(axes[i, 0], clockwise, LIM * 0.99, color)
            rotation_arrow(axes[i, 1], not clockwise, LIM * 0.99,
                           CCW_COLOR if clockwise else CW_COLOR)
        else:
            rotation_arrow(axes[i, 0], clockwise, LIM * 0.99, color)
        arrows(axes[i, 2], centers, uv, lum)
        axes[i, 2].set_title(flow_title, fontsize=11, pad=4)
        hexmap(axes[i, 3], centers, t, mask, np.percentile(np.abs(t[mask]), 97))
        rotation_arrow(axes[i, 3], clockwise, rmax * 1.12, color)
        axes[i, 3].set_title("Tangential component", fontsize=11, pad=4)
        axes[i, 3].text(0, LIM * 1.06, f"net {'clockwise' if clockwise else 'counterclockwise'}"
                        f"  ({'T' if img_b is None else 'A'} = {mean_t:+.4f})", ha="center",
                        va="top", fontsize=11, color=color, fontweight="bold")
        axes[i, 0].text(-0.12, 0.5, title, transform=axes[i, 0].transAxes, ha="right",
                        va="center", fontsize=12, fontweight="bold")
        for a in axes[i]:
            a.set_xlim(-LIM * 1.02, LIM * 1.02)
            a.set_ylim(LIM * 1.02, -LIM * 1.02)   # y downward, as on the screen
            a.set_aspect("equal")
            a.axis("off")
    cax = fig.add_axes([0.925, 0.42, 0.011, 0.16])
    cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=TwoSlopeNorm(0, -1, 1), cmap=CMAP),
                      cax=cax, ticks=[-1, 0, 1])
    cb.ax.set_yticklabels(["counter-\nclockwise", "0", "clockwise"])
    cb.outline.set_visible(False)
    fig.suptitle(f"Decoded flow averaged over frames 10–49, {label}. "
                 "Curved arrows: net direction of the model output.",
                 x=0.5, y=0.94, fontsize=11.5)
    out = ROOT / f"figures/fig01/fig01_flow_draft_{which}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    print(out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ensemble")
