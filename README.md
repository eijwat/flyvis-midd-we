# MIDD × FlyVis

[Revised manuscript, V6 (PDF)](manuscript/flyvis_midd_manuscript_V6.pdf) — revision made in this fork (2026-11-17): rewritten text, redrawn main and supplementary figures (`figures/**/*_main_V2.*`), plain-language supplementary tables. Source: `manuscript/manuscript_V6.md`. The author list is not yet filled in. See [Revision in this fork](#revision-in-this-fork).

[Original manuscript (PDF) ](manuscript/flyvis_midd_manuscript.pdf)

[Graphical Abstract ](manuscript/graphical.png)

This repository accompanies a study of decoded motion responses to physically static motion illusion-like discrete disk (MIDD) patterns in FlyVis networks trained for optical-flow estimation. It contains the manuscript, stimuli, analysis code, processed results, and figure notebooks.

本研究では、静止MIDD刺激に対するFlyVisネットワークのdecoded flowを調べます。日本語での概要は以下のとおりです。

本研究では、静止MIDD刺激から生じるdecoded motionを、Original/Mirror反対称成分 \(A\) と共有成分 \(S\) に分解し、実際の方向反転が \(|A|>|S|\) で決まることを示します。さらに、局所3MIDD応答から4MIDDの大域成分を予測できること、非線形motion-detector arrayが静止方向残差を生成しうること、そしてこの応答がMIDDを学習目標に含まないoptic-flow学習中に形成され、trained network–decoder pairingに依存することを示します。decoded flowはモデル出力であり、人間やハエの知覚を直接測定したものではありません。

### Research agents

- OpenAI GPT
- Google Gemini
- Anthropic Claude

## Main findings

- Static MIDD patterns evoke directional decoded flow in optic-flow-trained FlyVis networks (a model output, not perception).
- Under a centered eight-field rendering, the four-level antisymmetric scalar follows an affine prediction from three-level components: \(A_4 \approx \alpha\,[A_3(C_1)-A_3(C_2)]+\beta\) (scalar only, not vector-field additivity).
- Matched shuffles and other static controls give comparable or larger outputs, so the response is not MIDD-specific. A classical nonlinear Reichardt array partially reproduces its directional structure (a candidate account, not an identified mechanism).
- The antisymmetric component emerges during ordinary optic-flow learning, although MIDD is not a training target.
- Output varies across models, phase, and rendering, and depends on network–decoder pairing, consistent with distributed, task-general computation and co-adaptation rather than a dedicated MIDD circuit.

## Reproduce the figures

The canonical notebooks replay bundled processed inputs; they do not download pretrained networks or run FlyVis inference. Use Python 3.9 or newer:

```bash
git clone --branch main https://github.com/poxsalop5029/flyvis-midd.git
cd flyvis-midd
python -m pip install -e ".[all]" scipy pillow jupyterlab
python -m jupyter lab
```

Run the desired notebook from the repository root. Supplementary notebooks for S1–S10 are in [`notebooks/supplementary/`](notebooks/supplementary/). See the [reproduction guide](docs/reproduction_map.md) for inputs, outputs, and verification details.

## Main figures

| Figure | Topic | Notebook |
|---|---|---|
| Fig. 1 | Static MIDD and decoded flow | [Open](notebooks/fig01/fig_1.ipynb) |
| Fig. 2 | Luminance dependence and controls | [Open](notebooks/fig02/fig_2.ipynb) |
| Fig. 3 | Local-to-global scalar prediction | [Open](notebooks/fig03/fig_3.ipynb) |
| Fig. 4 | Phase, geometry, and shared components | [Open](notebooks/fig04/fig_4.ipynb) |
| Fig. 5 | Learning dynamics and task performance | [Open](notebooks/fig05/fig_5.ipynb) |
| Fig. 6 | Population interventions and readout | [Open](notebooks/fig06/fig_6.ipynb) |

## Repository structure

- `data/` — stimuli and processed analysis inputs
- `notebooks/` — main and supplementary figure notebooks
- `src/flyvis_midd/` — shared analysis and plotting code
- `figures/` — generated figures and numerical summaries
- `manuscript/` — manuscript, references, and PDF

## Revision in this fork

This fork (eijwat/flyvis-midd-we) revises the manuscript and figures of the original repository (poxsalop5029/flyvis-midd). The original files are kept unchanged; revised files have a version suffix.

- `manuscript/manuscript_V2.md` … `manuscript_V6.md` — successive revisions (latest: V6); `manuscript/manuscript.md` is the original
- `src/flyvis_midd/figure_rendering_v2.py`, `scripts/render_figures_v2.py` — redraw all 6 main and 10 supplementary figures from the stored tables (no FlyVis inference needed); output `figures/figNN/figNN_main_V2.*`
- `scripts/generate_fig1_flow_fields.py` — recomputes the decoded flow fields for the static MIDD stimuli (official 50 models, FlyVis 1.2.0, CPU) and stores them in `data/precomputed/fig01/fig1_flow_fields.npz`; the recomputed tangential flow matches the stored table to within 3e-7
- `scripts/draw_fig1_flow.py` — draft flow-field drawings used to check directions
- Figure numbers in the revised manuscript follow the order of the text: Fig. 1 ← `fig01`, Fig. 2 ← `fig05`, Fig. 3 ← `fig02`, Fig. 4 ← `fig03`, Fig. 5 ← `fig04`, Fig. 6 ← `fig06`

Build the revised PDF:

```bash
python3 scripts/build_manuscript_pdf.py --source manuscript/manuscript_V6.md --figure-suffix _V2 \
    --figure-order 1,5,2,3,4,6 --plain-tables --output manuscript/flyvis_midd_manuscript_V6.pdf
```

## Documentation

- [Reproduction map](docs/reproduction_map.md)
- [Processed-data provenance](data/precomputed/PROVENANCE.md)

## Repository maintainance

 `poxsalop5029`.

## License

Code is licensed under [MIT](LICENSE); original manuscript, figures, documentation, and research data are licensed under [CC BY 4.0](LICENSE-CONTENT.md). Third-party materials are excluded and retain their original licenses.
