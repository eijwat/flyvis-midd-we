#!/usr/bin/env python3
"""Revised main figures (V2). Reads stored inputs only; never loads a model.

Outputs are written next to the original figures as ``figNN_main_V2.pdf/png``;
the original ``figNN_main.*`` files and their manifests are left untouched.

    python scripts/render_figures_v2.py [1 2 … 6 S1 … S10]   (from the repository root)

Conventions: image coordinates (x rightward, y downward), clockwise-positive
tangential flow, decoder v negated once, as in ``flyvis_midd.rotation``.
"""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from flyvis_midd import figure_rendering as base  # noqa: E402
from flyvis_midd.stimuli import (  # noqa: E402
    build_3midd_sequences, build_4midd_sequences, render_sector_image)

GROUPS = ["3MIDD_048", "3MIDD_207", "4MIDD_085_170"]
LABELS = ["3MIDD C = 48", "3MIDD C = 207", "4MIDD 85/170"]
COLORS = ["#0072B2", "#D55E00", "#009E73"]
CW, CCW = "#c2410c", "#1d4ed8"          # clockwise warm, counterclockwise cool
ARROW = "#e11d1d"                        # flow vectors
CMAP = LinearSegmentedColormap.from_list("ccw_cw", [CCW, "#93b4f0", "#f1f1ee", "#f0a880", CW])
RC = {"font.size": 14, "font.family": "DejaVu Sans", "axes.spines.top": False,
      "axes.spines.right": False, "pdf.fonttype": 42, "ps.fonttype": 42,
      "axes.titlesize": 14, "axes.labelsize": 14, "xtick.labelsize": 12.5, "ytick.labelsize": 12.5}


def panel(ax, letter, title="", x=None, y=None, dy=7):
    """Panel letter and title on one line above the axes, never overlapping."""
    ax.annotate(letter, (0, 1), xycoords="axes fraction", xytext=(0, dy),
                textcoords="offset points", fontsize=18.2, fontweight="bold",
                ha="left", va="bottom", annotation_clip=False)
    if title:
        ax.annotate(title, (0, 1), xycoords="axes fraction", xytext=(25, dy + 1),
                    textcoords="offset points", fontsize=14.3, ha="left", va="bottom",
                    annotation_clip=False)
    if x:
        ax.set_xlabel(x)
    if y:
        ax.set_ylabel(y)


def zero(ax, vertical=False):
    ax.axhline(0, color=".6", lw=0.8, zorder=0)
    if vertical:
        ax.axvline(0, color=".6", lw=0.8, zorder=0)


def disk(ax, sequence, size=382):
    image, _ = render_sector_image(sequence, image_size=size, inner_diameter=55,
                                   outer_diameter=size)
    ax.imshow(image, cmap="gray", vmin=0, vmax=255, interpolation="lanczos")
    ax.axis("off")


def rotation_arrow(ax, clockwise, radius, color, lw=2.6):
    a0, a1 = (-150, -30) if clockwise else (-30, -150)
    p0 = radius * np.array([np.cos(np.deg2rad(a0)), np.sin(np.deg2rad(a0))])
    p1 = radius * np.array([np.cos(np.deg2rad(a1)), np.sin(np.deg2rad(a1))])
    ax.add_patch(FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={-0.45 if clockwise else 0.45}",
                                 arrowstyle="-|>", mutation_scale=20, lw=lw, color=color,
                                 clip_on=False, zorder=6))


def tangential(centers, uv):
    dy, dx = centers[:, 0], centers[:, 1]
    r = np.hypot(dx, dy)
    rr = np.maximum(r, 1e-9)
    t = uv[0] * (-dy / rr) + uv[1] * (dx / rr)
    return t, (r >= 0.14 * r.max()) & (r <= 0.98 * r.max()), r.max()


def field_axes(ax, lim=215):
    ax.set_xlim(-lim, lim)
    ax.set_ylim(lim, -lim)
    ax.set_aspect("equal")
    ax.axis("off")


def flow_panel(ax, centers, uv, lum=None, hexsize=120):
    if lum is not None:
        ax.scatter(centers[:, 1], centers[:, 0], c=lum, cmap="gray", vmin=0, vmax=1,
                   s=hexsize, marker="h", linewidths=0, alpha=0.5)
    scale = np.percentile(np.hypot(uv[0], uv[1]), 95) / 26.0
    ax.quiver(centers[:, 1], centers[:, 0], uv[0], uv[1], angles="xy", scale_units="xy",
              scale=scale, width=0.0075, headwidth=3.8, headlength=4.2, color=ARROW, zorder=3)
    field_axes(ax)


def map_panel(ax, centers, uv, hexsize=120):
    t, mask, rmax = tangential(centers, uv)
    vmax = np.percentile(np.abs(t[mask]), 97)
    ax.scatter(centers[~mask, 1], centers[~mask, 0], c="#e9e9e6", s=hexsize, marker="h", linewidths=0)
    ax.scatter(centers[mask, 1], centers[mask, 0], c=t[mask], cmap=CMAP,
               norm=TwoSlopeNorm(0, -vmax, vmax), s=hexsize, marker="h", linewidths=0)
    clockwise = t[mask].mean() > 0
    rotation_arrow(ax, clockwise, rmax * 1.1, CW if clockwise else CCW)
    field_axes(ax, 235)
    return t[mask].mean(), clockwise


def jitter(n, width=0.11):
    return width * np.sin(np.arange(n) * 2.4)


def fig1():
    d = pd.read_csv(ROOT / "data/precomputed/fig01/fig1_midd_per_model.csv")
    z = np.load(ROOT / "data/precomputed/fig01/fig1_flow_fields.npz")
    conditions = list(z["conditions"])
    centers = z["receptor_centers_yx"].astype(float)
    centers -= centers.mean(0)
    flow = z["mean_flow_uv"].astype(float).mean(0)           # mean of 50 models
    s1 = ROOT / "data/precomputed/supplementary/figS1"
    prop = np.load(s1 / "propeller_flow_50models.npy", mmap_mode="r")
    pr = np.load(s1 / "propeller_boxeye_rendered.npz")
    ps = np.load(s1 / "propeller_sequences.npz")
    i_cw = [i for i, n in enumerate(pr["names"]) if str(n).upper().startswith("CW")][0]
    pflow = np.asarray(prop[:, i_cw, 10:50], float).mean((0, 1))

    def image_uv(f):
        return np.stack([f[0], -f[1]])

    fig = plt.figure(figsize=(11.4, 15.4))
    outer = fig.add_gridspec(4, 1, height_ratios=[1.0, 1.25, 1.25, 1.0], hspace=0.2,
                             left=0.07, right=0.97, top=0.965, bottom=0.045)

    # A: stimuli
    gs = outer[0].subgridspec(1, 4, wspace=0.08)
    seqs = [("3MIDD, C = 48\nOriginal", build_3midd_sequences(48)["original"]),
            ("3MIDD, C = 48\nMirror", build_3midd_sequences(48)["mirror"]),
            ("3MIDD, C = 207\nOriginal", build_3midd_sequences(207)["original"]),
            ("4MIDD, 85/170\nOriginal", build_4midd_sequences(85, 170)["original"])]
    for k, (title, seq) in enumerate(seqs):
        ax = fig.add_subplot(gs[0, k])
        disk(ax, seq)
        ax.set_title(title, fontsize=14.3, pad=6)
        if k == 0:
            panel(ax, "A", dy=34)

    # B: physical rotation
    gs = outer[1].subgridspec(1, 3, wspace=0.04, width_ratios=[0.8, 1, 1])
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(ps["frames"][i_cw, 25], cmap="gray", vmin=0, vmax=1, interpolation="lanczos")
    ax.axis("off")
    ax.set_title("Propeller rotating clockwise", fontsize=14.3, pad=6)
    ax.set_anchor("C")
    panel(ax, "B", dy=22)
    ax = fig.add_subplot(gs[0, 1])
    flow_panel(ax, centers, image_uv(pflow), pr["luminance"][i_cw, 25, 0])
    ax.set_title("Decoded flow", fontsize=14.3, pad=6)
    ax = fig.add_subplot(gs[0, 2])
    mean_t, _ = map_panel(ax, centers, image_uv(pflow))
    ax.set_title("Tangential component", fontsize=14.3, pad=6)
    ax.text(0, 238, f"clockwise, T = {mean_t:.1f}", ha="center", va="top", fontsize=14.3,
            color=CW, fontweight="bold")

    # C: static patterns, Original/Mirror half-difference
    gs = outer[2].subgridspec(1, 4, wspace=0.03)
    for k, (group, label) in enumerate((("3MIDD_048", "3MIDD, C = 48"),
                                        ("3MIDD_207", "3MIDD, C = 207"))):
        o = conditions.index(group + "__original")
        m = conditions.index(group + "__mirror")
        uv = image_uv((flow[o] - flow[m]) / 2)
        ax = fig.add_subplot(gs[0, 2 * k])
        flow_panel(ax, centers, uv, hexsize=70)
        ax.set_title(f"Static {label}\nflow for Original", fontsize=13.7, pad=6)
        if k == 0:
            panel(ax, "C", dy=36)
        ax = fig.add_subplot(gs[0, 2 * k + 1])
        mean_a, clockwise = map_panel(ax, centers, uv, hexsize=70)
        ax.set_title("tangential\ncomponent", fontsize=13.7, pad=6)
        ax.text(0, 238, f"{'clockwise' if clockwise else 'counterclockwise'}, A = {mean_a:+.4f}",
                ha="center", va="top", fontsize=13.7, color=CW if clockwise else CCW,
                fontweight="bold")
    cax = fig.add_axes([0.985, 0.335, 0.008, 0.09])
    cb = fig.colorbar(matplotlib.cm.ScalarMappable(norm=TwoSlopeNorm(0, -1, 1), cmap=CMAP),
                      cax=cax, ticks=[-1, 1])
    cb.ax.set_yticklabels(["CCW", "CW"], fontsize=11.7)
    cb.outline.set_visible(False)

    # D, E: per-model summaries
    gs = outer[3].subgridspec(1, 2, wspace=0.3, width_ratios=[1, 1.25])
    q = d[d.group == GROUPS[0]]
    ax = fig.add_subplot(gs[0, 0])
    b = q.actual_reversal.to_numpy(bool)
    ax.scatter(q.T_original[b], q.T_mirror[b], s=34, color=COLORS[0], label=f"opposite signs ({b.sum()}/50)")
    ax.scatter(q.T_original[~b], q.T_mirror[~b], s=34, facecolors="none", edgecolors=COLORS[0],
               label=f"same sign ({(~b).sum()}/50)")
    zero(ax, True)
    ax.legend(fontsize=12.3, frameon=False, loc="upper right", bbox_to_anchor=(1.02, 1.0))
    panel(ax, "D", "3MIDD C = 48, one point per network", x="T, Original (clockwise +)",
          y="T, Mirror (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    for i, g in enumerate(GROUPS):
        v = d[d.group == g].A.to_numpy()
        ax.scatter(i + jitter(len(v), 0.16), v, s=26, color=COLORS[i], alpha=0.7)
        ax.plot([i - 0.25, i + 0.25], [v.mean()] * 2, color="black", lw=1.8)
        n_neg = int((v < 0).sum())
        ax.text(i, 0.062, f"{n_neg}/50 negative\n{50 - n_neg}/50 positive", ha="center",
                va="bottom", fontsize=12.3)
    ax.set_xticks(range(3), LABELS)
    ax.set_xlim(-0.62, 2.55)
    ax.set_ylim(-0.075, 0.085)
    zero(ax)
    panel(ax, "E", "Mirror-reversing component A", y="A (clockwise +)")
    return fig


def fig2():
    d = pd.read_csv(ROOT / "data/precomputed/fig01/fig1_midd_per_model.csv")
    l = pd.read_csv(ROOT / "data/precomputed/fig02/fig2B_luminance_A_per_model.csv")
    neg = pd.read_csv(ROOT / "data/precomputed/fig02/fig2E_negative_control_per_model.csv")
    sh = pd.read_csv(ROOT / "data/precomputed/fig02/official50_shuffle_model_metrics.csv")
    pv = l.pivot(index="model_id", columns="C", values="A")
    levels = list(pv.columns)

    fig = plt.figure(figsize=(11.4, 15.6))
    outer = fig.add_gridspec(4, 1, height_ratios=[0.78, 1.0, 0.95, 1.0], hspace=0.62,
                             left=0.09, right=0.97, top=0.965, bottom=0.05)

    # A: luminance series, five large disks
    shown = [16, 64, 128, 191, 239]
    gs = outer[0].subgridspec(1, 5, wspace=0.06)
    for k, c in enumerate(shown):
        ax = fig.add_subplot(gs[0, k])
        disk(ax, build_3midd_sequences(c)["original"])
        ax.set_title(f"C = {c}", fontsize=14.3, pad=5)
        if k == 0:
            panel(ax, "A", "", dy=20)

    # B: A against C; C: sign pattern
    gs = outer[1].subgridspec(1, 2, wspace=0.3, width_ratios=[1.35, 1])
    ax = fig.add_subplot(gs[0, 0])
    for _, row in pv.iterrows():
        ax.plot(levels, row.values, color=COLORS[0], alpha=0.22, lw=0.8)
    ax.plot(levels, pv.mean(0), color="black", lw=2.6, label="mean of 50 networks")
    zero(ax)
    for c in shown:
        ax.plot([c], [-0.079], marker="^", color=".35", ms=5, clip_on=False)
    ax.set_ylim(-0.08, 0.07)
    ax.legend(fontsize=12.3, frameon=False, loc="upper left")
    panel(ax, "B", "3MIDD, 15 intermediate luminances", x="Intermediate luminance C",
          y="A (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    a48, a207 = pv[48], pv[207]
    both = (a48 < 0) & (a207 > 0)
    ax.scatter(a48[both], a207[both], s=30, color=COLORS[0],
               label=f"negative at 48 and\npositive at 207 ({both.sum()}/50)")
    ax.scatter(a48[~both], a207[~both], s=30, facecolors="none", edgecolors=COLORS[0],
               label=f"other ({(~both).sum()}/50)")
    zero(ax, True)
    ax.legend(fontsize=11.7, frameon=False, loc="upper left", bbox_to_anchor=(-0.02, 1.02), handletextpad=0.2)
    panel(ax, "C", "Sign at dark versus light gray", x="A at C = 48", y="A at C = 207")

    # D: raw Original/Mirror outputs, one small panel per pattern
    gs = outer[2].subgridspec(1, 3, wspace=0.36)
    for i, g in enumerate(GROUPS):
        q = d[d.group == g]
        ax = fig.add_subplot(gs[0, i])
        b = q.actual_reversal.to_numpy(bool)
        ax.scatter(q.T_original[b], q.T_mirror[b], s=24, color=COLORS[i])
        ax.scatter(q.T_original[~b], q.T_mirror[~b], s=24, facecolors="none", edgecolors=COLORS[i])
        lim = 1.08 * max(q.T_original.abs().max(), q.T_mirror.abs().max())
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        zero(ax, True)
        title = f"{LABELS[i]}\nopposite signs: {b.sum()}/50"
        if i == 0:
            panel(ax, "D", title, x="T, Original", y="T, Mirror")
        else:
            ax.set_xlabel("T, Original")
            ax.annotate(title, (0, 1), xycoords="axes fraction", xytext=(25, 8),
                        textcoords="offset points", fontsize=14.3, ha="left", va="bottom")

    # E: balanced control; F: ordered versus shuffled
    gs = outer[3].subgridspec(1, 2, wspace=0.3, width_ratios=[1, 1.35])
    ax = fig.add_subplot(gs[0, 0])
    names = ["3MIDD 48", "3MIDD 207", "4MIDD 85/170"]
    for i, name in enumerate(names):
        v = neg[neg.condition == name].T_negative.to_numpy()
        ax.scatter(i + jitter(len(v), 0.16), v, s=24, color=COLORS[i], alpha=0.7)
        ax.plot([i - 0.25, i + 0.25], [v.mean()] * 2, color="black", lw=1.8)
    ax.set_xticks(range(3), ["3MIDD\nC = 48", "3MIDD\nC = 207", "4MIDD\n85/170"], fontsize=12.3)
    zero(ax)
    panel(ax, "E", "Balanced patterns", y="T (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    for i, g in enumerate(GROUPS):
        q = sh[sh.group == g].sort_values("model_id")
        x0, x1 = 3.6 * i, 3.6 * i + 1.5
        for _, row in q.iterrows():
            ax.plot([x0, x1], [row.canonical_reflection_abs_A, row.shuffle_mean_abs_A],
                    color=COLORS[i], alpha=0.22, lw=0.8)
        ax.scatter([x0] * len(q), q.canonical_reflection_abs_A, s=20, color=COLORS[i], zorder=3)
        ax.scatter([x1] * len(q), q.shuffle_mean_abs_A, s=20, facecolors="white",
                   edgecolors=COLORS[i], zorder=3)
        for x, v in ((x0, q.canonical_reflection_abs_A), (x1, q.shuffle_mean_abs_A)):
            ax.plot([x - 0.32, x + 0.32], [v.mean()] * 2, color="black", lw=1.8, zorder=4)
    ax.set_xticks([0, 1.5, 3.6, 5.1, 7.2, 8.7], ["ordered", "shuffled"] * 3, fontsize=11.5)
    for i, lab in enumerate(LABELS):
        ax.text(3.6 * i + 0.75, -0.13, lab, transform=ax.get_xaxis_transform(), ha="center",
                va="top", fontsize=13)
    ax.set_ylim(bottom=0)
    panel(ax, "F", "Ordered versus sector-shuffled disks", y="Magnitude of mirror-reversing\ncomponent")
    return fig


def dots(ax, values, labels, colors=None, paired=False, width=0.13, s=34):
    """One column of points per group, mean bar, optional lines joining the same unit."""
    arrays = [np.asarray(v, float) for v in values]
    if paired:
        for k in range(len(arrays[0])):
            ax.plot(np.arange(len(arrays)) + jitter(len(arrays[0]), width)[k],
                    [v[k] for v in arrays], color=".8", lw=0.8, zorder=1)
    for i, v in enumerate(arrays):
        c = (colors or COLORS)[i % len(colors or COLORS)]
        ax.scatter(i + jitter(len(v), width), v, s=s, color=c, alpha=0.75, zorder=2)
        ax.plot([i - 0.24, i + 0.24], [v.mean()] * 2, color="black", lw=2, zorder=3)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_xlim(-0.6, len(labels) - 0.4)


def strip(ax, sequence, x0, y0, width, height=0.5):
    n = len(sequence)
    for k, v in enumerate(sequence):
        ax.add_patch(plt.Rectangle((x0 + k * width / n, y0), width / n, height,
                                   facecolor=str(v / 255), edgecolor="none"))
    ax.add_patch(plt.Rectangle((x0, y0), width, height, fill=False, edgecolor=".4", lw=1))


def fig3():
    """Summation rule. Stored eight-field scalars are counterclockwise-positive;
    they are negated here so that every figure is clockwise-positive."""
    d3 = ROOT / "data/precomputed/fig03"
    m = pd.read_csv(d3 / "composition_model_metrics.csv").sort_values("model_id")
    v = pd.read_csv(d3 / "composition_cv_metrics.csv")
    c = pd.read_csv(d3 / "fig3_3MIDD_components_per_model.csv")
    p = pd.read_csv(d3 / "fig3_canonical_pair_predictions.csv")
    q = pd.read_csv(d3 / "comparator_model_metrics.csv")
    fig = plt.figure(figsize=(11.4, 13.2))
    outer = fig.add_gridspec(3, 1, height_ratios=[0.5, 1, 1], hspace=0.4,
                             left=0.1, right=0.97, top=0.96, bottom=0.07)
    # A: the rule
    ax = fig.add_subplot(outer[0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.2)
    ax.axis("off")
    dark, light = 80, 175
    strip(ax, [0, dark, 255] * 2 + [0], 0.1, 0.9, 2.6)
    strip(ax, [0, light, 255] * 2 + [0], 3.5, 0.9, 2.6)
    strip(ax, [0, dark, 255, light] * 2 + [0], 7.0, 0.9, 2.9)
    for x, text in ((1.4, "3MIDD, $C_1$"), (4.8, "3MIDD, $C_2$"), (8.45, "4MIDD, $C_1$ and $C_2$")):
        ax.text(x, 1.55, text, ha="center", va="bottom", fontsize=14)
    for x, text in ((1.4, "$A_3(C_1)$"), (3.1, "$-$"), (4.8, "$A_3(C_2)$"), (6.55, r"$\approx$"),
                    (8.45, "$A_4(C_1,C_2)$")):
        ax.text(x, 0.35, text, ha="center", va="center", fontsize=19)
    panel(ax, "A", "Summation rule tested (after Kobayashi & Watanabe 2023)", dy=2)
    # B, C
    gs = outer[1].subgridspec(1, 2, wspace=0.3)
    ax = fig.add_subplot(gs[0, 0])
    for _, g in c.groupby("model_id"):
        ax.plot(g.c, -g.a3, color=COLORS[0], alpha=0.3, lw=1)
    mean = c.groupby("c").a3.mean()
    ax.plot(mean.index, -mean.values, color="black", lw=2.6, label="mean of 10 networks")
    zero(ax)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    panel(ax, "B", "Three-level responses", x="Intermediate luminance C",
          y="$A_3$ (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    x, y = -p.a4_predicted, -p.a4_observed
    ax.scatter(x, y, s=18, alpha=0.4, color=COLORS[0], linewidths=0)
    xx = np.array([min(x.min(), y.min()), max(x.max(), y.max())])
    ax.plot(xx, xx, "--", color=".45", lw=1.4, label="equality")
    ax.plot(xx, -m.intercept.mean() + m.slope.mean() * xx, color=COLORS[1], lw=2,
            label="mean fit")
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    ax.text(0.97, 0.05, f"mean $R^2$ = {m.r2.mean():.2f}", transform=ax.transAxes,
            ha="right", fontsize=13)
    ax.text(0.97, 0.13, "21 pairs × 10 networks", transform=ax.transAxes, ha="right", fontsize=13)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    panel(ax, "C", "Four-level responses",
          x="$A_3(C_1)-A_3(C_2)$", y="Observed $A_4$")
    # D, E
    gs = outer[2].subgridspec(1, 2, wspace=0.3, width_ratios=[0.8, 1.2])
    ax = fig.add_subplot(gs[0, 0])
    cv = v[v.split == "LOLO"].sort_values("model_id")
    dots(ax, [m.r2, cv.cv_r2], ["fitted", "held-out\nluminance"], paired=True)
    ax.set_ylim(0, 1.03)
    panel(ax, "D", "Fit and prediction", y="$R^2$ per network")
    ax = fig.add_subplot(gs[0, 1])
    dots(ax, [q[q.predictor == k].sort_values("model_id").cv_r2 for k in ["P0", "P1", "P2", "P3"]],
         ["own\n$A_3$", "mean of other\nnetworks", "one other\nnetwork", "$C_1-C_2$\nonly"],
         colors=[COLORS[0], ".45", ".45", ".45"], paired=True)
    zero(ax)
    panel(ax, "E", "Which three-level responses predict $A_4$?", y="Held-out $R^2$")
    return fig


def fig4():
    d4 = ROOT / "data/precomputed/fig04"
    p = pd.read_csv(d4 / "official50_phase_pairs.csv")
    pm = pd.read_csv(d4 / "official50_phase_model_metrics.csv")
    ic = pd.read_csv(d4 / "official50_phase_reliability.csv").iloc[0]
    geom = pd.read_csv(d4 / "receptor_geometry.csv")
    roi = pd.read_csv(d4 / "radial_radial_model_phase_metrics.csv")
    e = pd.read_csv(d4 / "geometry_geometry_contrasts.csv")
    t4c = pd.read_csv(ROOT / "data/precomputed/supplementary/biological_constraints/A1/"
                      "t4c_cluster_midd_metrics.csv")
    fig = plt.figure(figsize=(11.4, 14.4))
    gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.32, left=0.11, right=0.97, top=0.96,
                          bottom=0.07)
    ax = fig.add_subplot(gs[0, 0])
    for _, g in p.groupby("model_id"):
        ax.plot(g.phase_index * 1.25, g.A, color=COLORS[0], alpha=0.22, lw=0.8)
    mean = p.groupby("phase_index").A.mean()
    ax.plot(mean.index * 1.25, mean.values, color="black", lw=2.6, label="mean of 50 networks")
    zero(ax)
    ax.set_ylim(top=0.062)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    panel(ax, "A", "3MIDD C = 48 at twelve phases", x="Rotation of the disk (degrees)",
          y="A (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    same = np.sign(pm.A_phase0) == np.sign(pm.A_mean)
    ax.scatter(pm.A_phase0[same], pm.A_mean[same], s=30, color=COLORS[0],
               label=f"same sign ({same.sum()}/50)")
    ax.scatter(pm.A_phase0[~same], pm.A_mean[~same], s=30, facecolors="none",
               edgecolors=COLORS[0], label=f"different sign ({(~same).sum()}/50)")
    zero(ax, True)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    ax.text(0.97, 0.05, f"ICC(A,1) = {ic.icc_absolute:.2f}", transform=ax.transAxes,
            ha="right", fontsize=13, bbox=dict(facecolor="white", edgecolor="none", pad=2))
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    panel(ax, "B", "Reference phase vs. phase average", x="A at the reference phase",
          y="A averaged over phases")
    ax = fig.add_subplot(gs[1, 0])
    image, _ = render_sector_image(build_3midd_sequences(48)["original"])
    ax.imshow(image, cmap="gray", vmin=0, vmax=255, extent=(-191, 191, 191, -191), alpha=0.75)
    ax.scatter(geom.x[~geom.outer_ROI], geom.y[~geom.outer_ROI], s=13, color="#f0b000",
               linewidths=0)
    ax.scatter(geom.x[geom.outer_ROI], geom.y[geom.outer_ROI], s=13, color=ARROW, linewidths=0)
    ax.set_xlim(-205, 205)
    ax.set_ylim(205, -205)
    ax.set_aspect("equal")
    ax.axis("off")
    panel(ax, "C", "721 receptors on the disk (red, outer ring)")
    ax = fig.add_subplot(gs[1, 1])
    qq = roi[(roi.group == GROUPS[0]) & (roi.phase_index == 0) &
             roi.ROI.isin(["full", "outer"])].pivot(index="model_id", columns="ROI", values="A")
    dots(ax, [qq.full, qq.outer], ["whole ring", "outer ring"], paired=True)
    zero(ax)
    panel(ax, "D", "Region analysed, 10 networks", y="A (clockwise +)")
    ax = fig.add_subplot(gs[2, 0])
    qq = e[(e.group == GROUPS[0]) & e["transform"].str.contains("minus|plus")].groupby(
        "model_id")[["normalized_error_A", "normalized_error_S"]].mean()
    dots(ax, [qq.normalized_error_A, qq.normalized_error_S],
         ["mirror-reversing\npart A", "shared\npart S"], paired=True)
    ax.set_ylim(bottom=0)
    panel(ax, "E", "Shift of the disk by ±3 pixels, 10 networks",
          y="Change / mean flow magnitude")
    ax = fig.add_subplot(gs[2, 1])
    t = t4c[t4c.group == GROUPS[0]]
    names = {0: "upward\n(as in the fly)", 1: "downward", 2: "untuned"}
    groups = [t[t.t4c_cluster_id == k].A_mean for k in (0, 1, 2)]
    dots(ax, groups, [f"{names[k]}\nn = {len(g)}" for k, g in zip((0, 1, 2), groups)],
         colors=[COLORS[0], ".45", ".45"], width=0.16)
    zero(ax)
    panel(ax, "F", "Networks grouped by T4c tuning", y="A averaged over phases")
    return fig


def fig5():
    d5 = ROOT / "data/precomputed/fig05"
    n = pd.read_csv(d5 / "learning_normalized_metrics.csv")
    e = pd.read_csv(d5 / "fig05_EPE_step_summary.csv")
    official = pd.read_csv(d5 / "official50_sintel_epe.csv").fixed_eval_epe.median()
    n = n[n.optimizer_step <= 100000].copy()
    n["k"] = n.optimizer_step / 1000
    e = e[e.optimizer_step <= 100000]
    fig = plt.figure(figsize=(11.4, 13.6))
    outer = fig.add_gridspec(3, 1, height_ratios=[0.8, 0.95, 1], hspace=0.5, left=0.11,
                             right=0.97, top=0.96, bottom=0.08)
    gs = outer[0].subgridspec(1, 2, wspace=0.3)
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(e.optimizer_step / 1000, e["median"], color="black", lw=2)
    ax.fill_between(e.optimizer_step / 1000, e.q25, e.q75, color=".8", linewidth=0)
    ax.axhline(official, color=COLORS[1], ls=":", lw=2)
    ax.text(100, official - 0.012, "median of the 50\npretrained networks", color=COLORS[1],
            ha="right", va="top", fontsize=12)
    ax.set_ylim(official - 0.14, None)
    panel(ax, "A", "Task error during training", x="Training step (×1000)",
          y="Sintel endpoint error")
    ax = fig.add_subplot(gs[0, 1])
    for i, g in enumerate(GROUPS):
        q = n[n.group == g].groupby("k").abs_A_norm
        ax.fill_between(q.median().index, q.quantile(0.25), q.quantile(0.75), color=COLORS[i],
                        alpha=0.18, linewidth=0)
        ax.plot(q.median().index, q.median(), color=COLORS[i], lw=2.2, label=LABELS[i])
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    panel(ax, "B", "Size of the response", x="Training step (×1000)",
          y="|A| / mean flow magnitude")
    gs = outer[1].subgridspec(1, 3, wspace=0.12)
    for i, g in enumerate(GROUPS):
        ax = fig.add_subplot(gs[0, i])
        for _, q in n[n.group == g].groupby("seed"):
            ax.plot(q.k, q.A, color=COLORS[i], alpha=0.35, lw=0.8)
        ax.plot(n[n.group == g].groupby("k").A.median(), color="black", lw=2.2)
        zero(ax)
        ax.set_ylim(-0.065, 0.13)
        ax.set_xlabel("Training step (×1000)")
        if i == 0:
            panel(ax, "C", LABELS[i], y="A (clockwise +)")
        else:
            ax.tick_params(labelleft=False)
            ax.annotate(LABELS[i], (0, 1), xycoords="axes fraction", xytext=(25, 8),
                        textcoords="offset points", fontsize=14.3, ha="left", va="bottom")
    gs = outer[2].subgridspec(1, 2, wspace=0.3, width_ratios=[1.25, 1])
    end = n[n.optimizer_step == 100000]
    ax = fig.add_subplot(gs[0, 0])
    vals = [end[end.group == g].A for g in GROUPS]
    dots(ax, vals, LABELS, width=0.16)
    for i, v in enumerate(vals):
        neg = int((v < 0).sum())
        ax.text(i, 0.066, f"{neg}/14 negative\n{14 - neg}/14 positive", ha="center", va="bottom",
                fontsize=12.3)
    ax.set_ylim(-0.03, 0.085)
    zero(ax)
    panel(ax, "D", "Sign after 100,000 steps, 14 networks", y="A (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    init = n[n.optimizer_step == 0]
    for i, g in enumerate(GROUPS):
        a0 = init[init.group == g].A.abs().to_numpy()
        a1 = end[end.group == g].A.abs().to_numpy()
        for u, w in zip(a0, a1):
            ax.plot([i - 0.2, i + 0.2], [u, w], color=COLORS[i], alpha=0.4, lw=0.9)
        ax.scatter([i - 0.2] * len(a0), a0, s=24, color=COLORS[i], zorder=3)
        ax.scatter([i + 0.2] * len(a1), a1, s=24, facecolors="white", edgecolors=COLORS[i], zorder=3)
    ax.set_yscale("log")
    ax.set_xticks(range(3), ["3MIDD\nC = 48", "3MIDD\nC = 207", "4MIDD\n85/170"])
    panel(ax, "E", "Before (filled) and after training", y="|A| (log scale)")
    return fig


def fig6():
    from matplotlib.patches import FancyBboxPatch, Rectangle
    from flyvis_midd.figure_analysis import fig6_panel_data
    d6 = ROOT / "data/precomputed/fig06"
    names = ["replacement_metrics.csv", "crossswap_metrics.csv", "crossswap_direction_accuracy.csv"]
    data = fig6_panel_data({k: pd.read_csv(d6 / k) for k in names})
    fig = plt.figure(figsize=(11.4, 14.2))
    outer = fig.add_gridspec(3, 1, height_ratios=[0.5, 1, 1.15], hspace=0.42, left=0.11,
                             right=0.97, top=0.96, bottom=0.08)
    # A: schematic
    ax = fig.add_subplot(outer[0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.6)
    ax.axis("off")
    boxes = [(0.2, "Recurrent\nnetwork"), (2.75, "Activity of\n34 cell types"), (5.3, "Decoder"),
             (7.85, "Decoded\nflow")]
    for x0, label in boxes:
        ax.add_patch(FancyBboxPatch((x0, 1.25), 1.9, 1.0, boxstyle="round,pad=0.05",
                                    facecolor="#f3f5f7", edgecolor="#536273", lw=1.2))
        ax.text(x0 + 0.95, 1.75, label, ha="center", va="center", fontsize=13.5)
    for x0 in (2.2, 4.75, 7.3):
        ax.annotate("", xy=(x0 + 0.5, 1.75), xytext=(x0, 1.75),
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color=".3"))
    ax.annotate("", xy=(3.7, 1.2), xytext=(3.7, 0.55),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLORS[0]))
    ax.text(3.7, 0.3, "B, C: T4 or T4+T5 activity replaced by\nthe activity for a uniform gray field",
            ha="center", va="center", fontsize=12.5, color=COLORS[0])
    ax.annotate("", xy=(6.25, 1.2), xytext=(6.25, 0.55),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLORS[1]))
    ax.text(7.6, 0.3, "D, E: decoder taken from\nanother network", ha="center", va="center",
            fontsize=12.5, color=COLORS[1])
    panel(ax, "A", "Two interventions on the trained model", dy=0)
    # B, C
    gs = outer[1].subgridspec(1, 2, wspace=0.3, width_ratios=[0.8, 1.2])
    b = data["panel_b_intervention"]
    ax = fig.add_subplot(gs[0, 0])
    dots(ax, [b[b.intervention == k].sort_values("model_id").normalized_change
              for k in ("T4", "T4_T5")], ["T4", "T4+T5"], colors=[COLORS[0], COLORS[1]],
         paired=True)
    zero(ax)
    panel(ax, "B", "Static 3MIDD, C = 48", x="Cell types replaced",
          y="Change in A / mean flow magnitude")
    c = data["panel_c_physical"]
    ax = fig.add_subplot(gs[0, 1])
    positions = [("propeller", "T4", 0), ("propeller", "T4_T5", 1), ("edge", "T4", 2.6),
                 ("edge", "T4_T5", 3.6)]
    for cond, k, x in positions:
        v = c[(c.condition == cond) & (c.intervention == k)].sort_values("model_id").normalized_change
        ax.scatter(x + jitter(len(v), 0.1), v, s=34, color=COLORS[0] if k == "T4" else COLORS[1],
                   alpha=0.75)
        ax.plot([x - 0.24, x + 0.24], [v.mean()] * 2, color="black", lw=2)
    ax.set_xticks([0, 1, 2.6, 3.6], ["T4", "T4+T5", "T4", "T4+T5"])
    for x, text in ((0.5, "rotating propeller"), (3.1, "moving edge")):
        ax.text(x, 1.0, text, transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=13)
    ax.set_ylim(top=1.1)
    zero(ax)
    panel(ax, "C", "Physical motion", x="Cell types replaced",
          y="Change in response /\nmean flow magnitude")
    # D, E
    gs = outer[2].subgridspec(1, 2, wspace=0.34, width_ratios=[0.8, 1.2])
    d = data["panel_d_pairing"].sort_values("network_id")
    ax = fig.add_subplot(gs[0, 0])
    dots(ax, [d.matched_abs_A, d.mismatched_mean_abs_A], ["own\ndecoder", "other decoders\n(mean of 9)"],
         colors=[COLORS[0], COLORS[1]], paired=True, width=0.05)
    ax.set_ylim(bottom=0)
    panel(ax, "D", "Static 3MIDD, C = 48", y="|A|")
    e = data["panel_e_direction"]
    ids = sorted(e.network_id.unique())
    matrix = e.pivot(index="network_id", columns="decoder_id", values="both_correct").reindex(
        index=ids, columns=ids).to_numpy(bool)
    ax = fig.add_subplot(gs[0, 1])
    ax.imshow(matrix, cmap=matplotlib.colors.ListedColormap(["#ececea", "#007f5f"]), vmin=0,
              vmax=1)
    ax.set_xticks(range(10), [f"{k:03d}" for k in ids], rotation=90)
    ax.set_yticks(range(10), [f"{k:03d}" for k in ids])
    for k in range(10):
        ax.add_patch(Rectangle((k - 0.5, k - 0.5), 1, 1, fill=False, edgecolor="black", lw=1.6))
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    off = int(matrix.sum() - np.trace(matrix))
    panel(ax, "E", f"Both grating directions decoded (green)",
          x=f"Decoder\nown decoder (outlined): {int(np.trace(matrix))}/10\nother decoders: {off}/90",
          y="Network")
    return fig


# ---------------------------------------------------------------- supplementary figures
SUPP = ROOT / "data/precomputed/supplementary"

# Plain-language panel headers for the supplementary figures whose plotting code is
# reused from flyvis_midd.figure_rendering: {figure: {letter: (title, xlabel, ylabel)}}.
# None keeps the original text.
HEADERS = {
    "S3": {"A": ("50 networks, first second", "Time (s)", "Mean A"),
           "B": ("Three networks, 10 s: A", "Time (s)", "A"),
           "C": ("Three networks, 10 s: S", "Time (s)", "S"),
           "D": ("Three networks, 10 s: T", "Time (s)", "T (dashed, Mirror)"),
           "E": ("Early versus late window", None, "A, 3MIDD C = 48"),
           "F": ("Effect of fade-in duration", "Fade-in duration (s)", "A at 9–10 s"),
           "G": ("Effect of image jitter", "Jitter amplitude (pixels)", "|A| at 9–10 s"),
           "H": ("Balanced and uniform images", None, "T at 9–10 s")},
    "S5": {"A": ("Ordered minus shuffled disks", None, "Difference in |A|"),
           "B": ("Rank of the ordered disk", None, "Percentile among ten shuffles"),
           "C": ("Static patterns and rotation", None, "|Paired contrast| / flow magnitude"),
           "D": ("Uniform and balanced images", None, "T / flow magnitude"),
           "E": ("Shared component S, 10 networks", "Rotation of the disk (degrees)", "S (clockwise +)"),
           "F": ("Opposite signs across phases", None, "Fraction of phases"),
           "G": ("Task error and A", "Sintel endpoint error", "A at the reference phase"),
           "H": ("Task error and phase variability", "Sintel endpoint error", "SD of A across phases /\nflow magnitude")},
    "S6": {k: (None, "Pattern period / receptor spacing", y) for k, y in zip(
        "ABCDEFGHI", ["A"] * 3 + ["|A| / flow magnitude"] * 3 + ["S"] * 3)},
    "S7": {"A": ("Held-out prediction: R²", None, "Held-out R²"),
           "B": ("Held-out prediction: error", None, "Held-out RMSE"),
           "C": ("Held-out prediction: sign", None, "Fraction of signs correct"),
           "D": ("Fitted slope", None, "Slope"),
           "E": ("Fitted intercept", None, "Intercept (stored sign)"),
           "F": ("Comparison with random smooth curves", None, "Own minus random, held-out R²")},
    "S8": {"A": ("Networks crossing a threshold", "|A| threshold", "Networks (of 14)"),
           "B": ("Step at which it is crossed", "|A| threshold", "Training step (×1000)"),
           "C": ("A during training", "Training step (×1000)", "A (clockwise +)"),
           "D": ("|A| − |S| during training", "Training step (×1000)", "|A| − |S|"),
           "E": ("Ordered, shuffled, balanced", "Training step (×1000)", "|Paired contrast| /\nflow magnitude"),
           "F": ("Uniform gray field", "Training step (×1000)", "T / flow magnitude"),
           "G": ("Rotating propeller, 3 networks", "Training step (×1000)", "CW minus CCW response"),
           "H": ("Moving edge, 3 networks", "Training step (×1000)", "Right minus left response")},
    "S9": {"A": ("Control replacements", None, "Change in A / flow magnitude"),
           "B": ("Activity and decoded A", None, "Spearman ρ within network"),
           "C": ("Replacement by mean activity", None, "Loss of the response"),
           "D": ("Silencing in the network: task", None, "Change in Sintel error"),
           "E": ("Response remaining", None, "Fraction of the response"),
           "F": ("Flow magnitude, no replacement", None, "Mean flow magnitude"),
           "G": ("T4 subtype activity", "Intermediate luminance C", "Normalized activity"),
           "H": ("Silencing in the network: A", None, "Change in A")},
    "S10": {"A": ("A for every pair", "Decoder", "Network"),
            "B": ("Grating response for every pair", "Decoder", "Network"),
            "C": ("Sources of variation in A", None, "Share of variation (%)"),
            "D": ("Sources of variation, grating", None, "Share of variation (%)"),
            "E": ("Own versus other decoders", None, "|A|"),
            "F": ("Both grating directions decoded", "Decoder (black, correct)", "Network")},
}
WORDS = {"Canonical": "ordered", "Shuffle": "shuffled", "Random": "random", "Propeller": "propeller",
         "Uniform": "uniform", "Balanced negative": "balanced", "Uniform gray": "uniform",
         "Own A3": "own", "Other mean": "mean of\nothers", "All donors": "one\nother", "Delta C": "C1 − C2",
         "Matched": "own decoder", "Mean mismatch": "other decoders", "MIDD": "ordered",
         "shuffle": "shuffled", "negative": "balanced", "Twelve-phase fraction": "50 networks",
         "all_input": "all inputs", "T4_T5": "T4+T5", "T4_family": "T4 (all)", "slope": "",
         "intercept": "", "C48": "C = 48", "C207": "C = 207", "Early 0.2–1 s": "0.2–1 s",
         "Late 9–10 s": "9–10 s", "Lengthscale 0.25": "0.25", "Lengthscale 0.1": "0.1",
         "Lengthscale 0.5": "0.5", "Full annulus": "whole ring", "Outer ROI": "outer ring",
         "Network": "network", "Decoder": "decoder", "Residual": "interaction"}


def restyled_supp(key):
    """Supplementary figure drawn by the original code, with readable headers."""
    table = HEADERS[key]

    def new_panel(ax, letter, title, x=None, y=None):
        t, nx, ny = table.get(letter, (None, None, None))
        panel(ax, letter, title if t is None else t, nx if nx is not None else x,
              ny if ny is not None else y)
        ax.tick_params(labelsize=11)

    old = base.panel
    base.panel = new_panel
    try:
        base.INPUTS.clear()
        base.CHECKS.clear()
        fig = {"S3": base.supp3, "S5": base.supp5, "S6": base.supp6, "S7": base.supp7,
               "S8": base.supp8, "S9": base.supp9, "S10": base.supp10}[key]()
    finally:
        base.panel = old
    for ax in fig.axes:
        labels = [t.get_text() for t in ax.get_xticklabels()]
        if any(label in WORDS for label in labels):      # categorical axes only
            ax.set_xticks(ax.get_xticks(), [WORDS.get(label, label) for label in labels],
                          rotation=0, ha="center")
        elif any(t.get_rotation() not in (0, 90) for t in ax.get_xticklabels()):
            ax.tick_params(axis="x", rotation=0)
        legend = ax.get_legend()
        if legend is not None:
            for text in legend.get_texts():
                text.set_text(WORDS.get(text.get_text(), text.get_text()))
                text.set_fontsize(10)
            legend.set_frame_on(False)
        for text in list(ax.texts):      # drop working notes written inside the axes
            if text.get_transform() == ax.transAxes and text.get_position()[1] < 0.9:
                text.remove()
    width = fig.get_size_inches()[0]
    fig.set_size_inches(width, fig.get_size_inches()[1] * 1.22)
    fig.get_layout_engine().set(h_pad=0.2, hspace=0.08, wspace=0.06)
    return fig


def supp1():
    s1 = SUPP / "figS1"
    ps = np.load(s1 / "propeller_sequences.npz")
    names = [str(n) for n in ps["names"]]
    m = pd.read_csv(ROOT / "figures/supplementary/figS1/figS1_model_metrics.csv")
    det = pd.read_csv(ROOT / "figures/supplementary/figS1/figS1_rotation_detection.csv")
    cal = pd.read_csv(s1 / "multifield_sign_correspondence.csv")
    fig = plt.figure(figsize=(11.4, 11.6))
    outer = fig.add_gridspec(3, 1, height_ratios=[0.75, 1, 1], hspace=0.45, left=0.11, right=0.97,
                             top=0.95, bottom=0.07)
    gs = outer[0].subgridspec(1, 3, wspace=0.08)
    titles = {"Static": "Stationary", "CW_mid": "Rotating clockwise", "CCW_mid": "Rotating counterclockwise"}
    for k, name in enumerate(names):
        ax = fig.add_subplot(gs[0, k])
        ax.imshow(ps["frames"][k, 25], cmap="gray", vmin=0, vmax=1)
        ax.axis("off")
        ax.set_title(titles.get(name, name), fontsize=13, pad=5)
        if k == 0:
            panel(ax, "A", dy=22)
    gs = outer[1].subgridspec(1, 2, wspace=0.3)
    piv = m.pivot(index="model_id", columns="condition", values="mean_signed_tangent")
    ax = fig.add_subplot(gs[0, 0])
    dots(ax, [piv["CCW_mid"], piv["Static"], piv["CW_mid"]],
         ["counter-\nclockwise", "stationary", "clockwise"],
         colors=[CCW, ".45", CW], paired=True)
    zero(ax)
    panel(ax, "B", "Decoded rotation, 50 networks", y="T (clockwise +)")
    ax = fig.add_subplot(gs[0, 1])
    ok = det.rotation_flow_detected.to_numpy(bool)
    ax.scatter(det.minimum_absolute_tangent_ratio[ok], det.minimum_moving_to_static_magnitude_ratio[ok],
               s=30, color=COLORS[0], label=f"criteria met ({ok.sum()}/50)")
    ax.scatter(det.minimum_absolute_tangent_ratio[~ok], det.minimum_moving_to_static_magnitude_ratio[~ok],
               s=30, facecolors="none", edgecolors=COLORS[1], label=f"not met ({(~ok).sum()}/50)")
    ax.axvline(0.1, color=".5", ls="--", lw=1)
    ax.axhline(3, color=".5", ls="--", lw=1)
    ax.set_yscale("log")
    ax.set_xlim(0, 1.02)
    ax.legend(fontsize=12, frameon=False, loc="lower center")
    panel(ax, "C", "Detection criteria (dashed)", x="|T| / flow magnitude (smaller direction)",
          y="Flow magnitude, moving / stationary")
    gs = outer[2].subgridspec(1, 2, wspace=0.3)
    for k, (renderer, title) in enumerate((("single", "Single-eye rendering"),
                                           ("multi", "Eight-field rendering"))):
        q = cal[cal.renderer == renderer].sort_values("model_id")
        ax = fig.add_subplot(gs[0, k])
        dots(ax, [q.CW_scalar, q.CCW_scalar], ["clockwise", "counter-\nclockwise"],
             colors=[CW, CCW], paired=True)
        zero(ax)
        panel(ax, "D" if k == 0 else "E", f"{title}, 10 networks", y="Stored scalar")
    return fig


def supp2():
    s2 = SUPP / "figS2"
    st = pd.read_csv(s2 / "scalar_02_model_level_statistics.csv")
    pr = pd.read_csv(s2 / "scalar_03_canonical_pair_predictions.csv")
    fl = pd.read_csv(s2 / "field_02_representation_level_summary.csv")
    names = ["native\nresolution", "high\nresolution"]
    cols = [COLORS[0], COLORS[1]]

    def pair(table, column):
        t = table.pivot(index="model_id", columns="rendering", values=column)
        return [t["boxeye"], t["highres_232"]]

    fig = plt.figure(figsize=(11.4, 12.4))
    gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.32, left=0.11, right=0.97, top=0.95, bottom=0.07)
    ax = fig.add_subplot(gs[0, 0])
    dots(ax, pair(st, "r2"), names, colors=cols, paired=True)
    ax.set_ylim(0, 1.03)
    panel(ax, "A", "Summation rule, seven fields", y="$R^2$ per network")
    ax = fig.add_subplot(gs[0, 1])
    dots(ax, pair(st, "sign_accuracy"), names, colors=cols, paired=True)
    ax.set_ylim(0, 1.03)
    panel(ax, "B", "Sign of the prediction", y="Fraction of signs correct")
    for k, (rendering, label) in enumerate((("boxeye", "native resolution"),
                                            ("highres_232", "high resolution"))):
        q = pr[(pr.rendering == rendering) & (pr.model_id == pr.model_id.iloc[0])]
        ax = fig.add_subplot(gs[1, k])
        ax.scatter(q.a4_predicted, q.a4_observed, s=34, color=cols[k])
        lim = np.array([min(q.a4_predicted.min(), q.a4_observed.min()),
                        max(q.a4_predicted.max(), q.a4_observed.max())])
        ax.plot(lim, lim, "--", color=".45", lw=1.4)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
        panel(ax, "C" if k == 0 else "D", f"Network 000, {label}",
              x="$A_3(C_1)-A_3(C_2)$", y="Observed $A_4$")
    ax = fig.add_subplot(gs[2, 0])
    dots(ax, pair(fl, "mean_normalized_vector_rmse"), names, colors=cols, paired=True)
    ax.axhline(1, color=".6", lw=0.8, ls=":")
    ax.set_ylim(bottom=0)
    panel(ax, "E", "Whole flow field: error", y="RMSE / RMS of prediction")
    ax = fig.add_subplot(gs[2, 1])
    dots(ax, pair(fl, "mean_vector_cosine"), names, colors=cols, paired=True)
    zero(ax)
    ax.set_ylim(top=1)
    panel(ax, "F", "Whole flow field: direction", y="Cosine similarity")
    return fig


def supp4():
    s4 = SUPP / "figS4"
    comp = pd.read_csv(s4 / "model_comparison_summary.csv").set_index(["stimulus", "model"])
    rot = pd.read_csv(s4 / "known_rotation_sign_calibration.csv")
    sta = pd.read_csv(s4 / "calibrated_static_sign_comparison.csv")
    dec = pd.read_csv(s4 / "mirror_decomposition.csv")
    met = pd.read_csv(s4 / "raw_vs_directional_metrics.csv").set_index("analysis")
    mm = pd.read_csv(s4 / "mirror_directional_metrics.csv").iloc[0]
    arr, fly = COLORS[0], COLORS[1]
    fig = plt.figure(figsize=(11.4, 13.2))
    gs = fig.add_gridspec(3, 2, hspace=0.5, wspace=0.34, left=0.11, right=0.97, top=0.95, bottom=0.07)

    def bars(ax, groups, series, values, colors):
        w = 0.8 / len(series)
        for k, (name, color) in enumerate(zip(series, colors)):
            ax.bar(np.arange(len(groups)) + (k - (len(series) - 1) / 2) * w, values[k], w * 0.92,
                   color=color, label=name)
        ax.set_xticks(range(len(groups)), groups)

    ax = fig.add_subplot(gs[0, 0])
    vals = [[comp.loc[(s, m), "mean_abs"] for m in ("reichardt_array_linear", "bach_shift")]
            for s in ("3midd", "4midd")]
    bars(ax, ["linear pooling", "saturation\nbefore pooling"], ["3MIDD", "4MIDD"], vals, [".3", ".65"])
    ax.set_yscale("symlog", linthresh=1e-4)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    panel(ax, "A", "Detector array, static patterns", y="|Output|")
    ax = fig.add_subplot(gs[0, 1])
    vals = [rot.bach_cw_calibrated / rot.bach_cw_calibrated.abs().max(),
            rot.flyvis_cw_calibrated / rot.flyvis_cw_calibrated.abs().max()]
    bars(ax, ["clockwise", "counterclockwise"], ["detector array", "FlyVis network 000"], vals,
         [arr, fly])
    zero(ax)
    ax.legend(fontsize=12, frameon=False, loc="upper right")
    panel(ax, "B", "Physical rotation", y="Output (normalized, clockwise +)")
    ax = fig.add_subplot(gs[1, 0])
    vals = [sta.bach_cw_calibrated / sta.bach_cw_calibrated.abs().max(),
            sta.flyvis_cw_calibrated / sta.flyvis_cw_calibrated.abs().max()]
    bars(ax, ["3MIDD C = 48", "4MIDD 85/170"], ["detector array", "FlyVis network 000"], vals,
         [arr, fly])
    zero(ax)
    ax.set_ylim(0, 1.38)
    ax.set_yticks([0, 0.5, 1])
    ax.legend(fontsize=12, frameon=False, loc="upper right")
    panel(ax, "C", "Static patterns", y="Output (normalized, clockwise +)")
    sub = gs[1, 1].subgridspec(1, 2, wspace=0.12)
    n = int(np.sqrt(len(dec)))
    for k, (column, title) in enumerate((("bach_directional", "detector array"),
                                         ("flyvis_directional", "FlyVis 000"))):
        z = dec.pivot(index="g2", columns="g1", values=column).to_numpy()
        ax = fig.add_subplot(sub[0, k])
        ax.imshow(z / np.abs(z).max(), cmap=CMAP, vmin=-1, vmax=1, origin="lower", extent=(0, 1, 0, 1))
        ax.set_xlabel("$C_1$ / 255")
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.set_title(title, fontsize=12.5, pad=5)
        for side in ("top", "right"):
            ax.spines[side].set_visible(True)
        if k == 0:
            ax.set_ylabel("$C_2$ / 255")
            panel(ax, "D", "4MIDD, mirror-reversing part", dy=24)
        else:
            ax.tick_params(labelleft=False)
    ax = fig.add_subplot(gs[2, 0])
    vals = [[met.loc[a, c] for c in ("pearson_r", "spearman_rho", "robust_sign_agreement")]
            for a in ("raw", "mirror_antisymmetric")]
    bars(ax, ["Pearson r", "Spearman ρ", "sign\nagreement"], ["raw output", "mirror-reversing part"],
         vals, [".65", COLORS[2]])
    ax.set_ylim(0, 1)
    ax.legend(fontsize=12, frameon=False, loc="upper left")
    panel(ax, "E", "Agreement over the 21 × 21 grid", y="Array versus FlyVis")
    ax = fig.add_subplot(gs[2, 1])
    ax.bar([0, 1], [mm.flyvis_directional_rms, mm.flyvis_symmetric_rms], 0.6, color=[COLORS[2], ".65"])
    ax.set_xticks([0, 1], ["mirror-reversing\npart", "shared\npart"])
    panel(ax, "F", "FlyVis 000, size of the two parts", y="RMS over the grid")
    return fig


def render(key):
    plt.rcParams.update(RC)
    main = {"1": fig1, "2": fig2, "3": fig3, "4": fig4, "5": fig5, "6": fig6}
    new_supp = {"S1": supp1, "S2": supp2, "S4": supp4}
    if key in main:
        fig, out, stem = main[key](), ROOT / f"figures/fig{key.zfill(2)}", f"fig{key.zfill(2)}"
    else:
        fig = new_supp[key]() if key in new_supp else restyled_supp(key)
        out, stem = ROOT / f"figures/supplementary/fig{key}", f"fig{key}"
    fig.savefig(out / f"{stem}_main_V2.pdf", bbox_inches="tight")
    fig.savefig(out / f"{stem}_main_V2.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", out / f"{stem}_main_V2.png")


ALL = ["1", "2", "3", "4", "5", "6"] + [f"S{k}" for k in range(1, 11)]

if __name__ == "__main__":
    for k in sys.argv[1:] or ALL:
        render(k)
