---
layout: default
title: MIDD × FlyVis
---

# MIDD × FlyVis

**Illusory-motion signals emerge in a connectome-constrained model of the fly visual system trained on optic flow**

We study how FlyVis networks, whose wiring follows the fly visual connectome and which are trained only to estimate optic flow, respond to static motion illusion-like discrete design (MIDD) patterns.

## Main findings

- **The response is learned.** At initialization the direction-dependent rotational component $A$ of the decoded flow is absent ($|A|<3\times10^{-9}$). It appears during ordinary optic-flow training, although no MIDD is in the training set.
- **Luminance sets the direction.** For three-level patterns, $A$ is negative when the intermediate sector is dark gray (43 of 50 pretrained networks) and positive when it is light gray (40 of 50). Networks trained from scratch show the same signs (12/14 and 13/14).
- **A summation rule links three-level and four-level patterns.** The response to a four-level pattern follows from the difference between the responses to its two three-level components, $A_4 \approx \alpha\,[A_3(C_1)-A_3(C_2)]+\beta$ (mean $R^2=0.93$, held-out $R^2=0.90$), as described for human observers by Kobayashi & Watanabe (2023).
- **The rule is shared; the amounts are individual.** Networks with identical wiring differ in the sign and size of their responses and keep their relative ordering across stimulus phases (ICC 0.76). Each network's own three-level responses predict its four-level responses.
- **The response belongs to the motion pathway and its readout.** It changes when T4/T5 activity is replaced and when networks and decoders are exchanged, and it is also evoked by other static patterns. It is about three orders of magnitude smaller than the response to physical rotation.

Decoded flow is the output of the model, which we compare with human psychophysics; it is not itself a measurement of perception.

## Manuscript

[Read the manuscript (PDF)](https://github.com/eijwat/flyvis-midd-we/blob/main/manuscript/flyvis_midd_manuscript_V6.pdf) · [Repository](https://github.com/eijwat/flyvis-midd-we)

## Reproduce

All figures are drawn from bundled processed results without running FlyVis inference (`python scripts/render_figures_v2.py`). See the [reproduction guide](reproduction_map.md) for the input and output map of the original notebooks.

| Figure | Topic | Image | Notebook of the original version |
|---|---|---|---|
| Fig. 1 | Static MIDD patterns and the decoded flow | [PNG](https://github.com/eijwat/flyvis-midd-we/blob/main/figures/fig01/fig01_main_V2.png) | [fig_1](https://github.com/eijwat/flyvis-midd-we/blob/main/notebooks/fig01/fig_1.ipynb) |
| Fig. 2 | The response emerges during optic-flow training | [PNG](https://github.com/eijwat/flyvis-midd-we/blob/main/figures/fig05/fig05_main_V2.png) | [fig_5](https://github.com/eijwat/flyvis-midd-we/blob/main/notebooks/fig05/fig_5.ipynb) |
| Fig. 3 | The intermediate luminance sets the direction | [PNG](https://github.com/eijwat/flyvis-midd-we/blob/main/figures/fig02/fig02_main_V2.png) | [fig_2](https://github.com/eijwat/flyvis-midd-we/blob/main/notebooks/fig02/fig_2.ipynb) |
| Fig. 4 | Summation rule from three-level to four-level patterns | [PNG](https://github.com/eijwat/flyvis-midd-we/blob/main/figures/fig03/fig03_main_V2.png) | [fig_3](https://github.com/eijwat/flyvis-midd-we/blob/main/notebooks/fig03/fig_3.ipynb) |
| Fig. 5 | Variation with stimulus phase, sampling, and network | [PNG](https://github.com/eijwat/flyvis-midd-we/blob/main/figures/fig04/fig04_main_V2.png) | [fig_4](https://github.com/eijwat/flyvis-midd-we/blob/main/notebooks/fig04/fig_4.ipynb) |
| Fig. 6 | Motion pathway and readout | [PNG](https://github.com/eijwat/flyvis-midd-we/blob/main/figures/fig06/fig06_main_V2.png) | [fig_6](https://github.com/eijwat/flyvis-midd-we/blob/main/notebooks/fig06/fig_6.ipynb) |

## Code and data

The [GitHub repository](https://github.com/eijwat/flyvis-midd-we) contains the analysis code, stimuli, processed results, and figures. It is a fork of [poxsalop5029/flyvis-midd](https://github.com/poxsalop5029/flyvis-midd). For processed-data sources, see [`data/precomputed/PROVENANCE.md`](https://github.com/eijwat/flyvis-midd-we/blob/main/data/precomputed/PROVENANCE.md).
