# Illusory-motion signals emerge in a connectome-constrained model of the fly visual system trained on optic flow

## Abstract

Stationary patterns with repeating asymmetric luminance steps appear to move, and both humans and flies respond to them. We asked whether such responses arise in FlyVis, a recurrent network whose wiring follows the fly visual connectome and which is trained only to estimate optic flow from naturalistic video. We presented static motion illusion-like discrete design (MIDD) disks, previously used in human psychophysics, and read out the decoded flow. At initialization the direction-dependent rotational component was absent ($|A|<3\times10^{-9}$); it appeared during ordinary optic-flow training, although no MIDD was in the training set. Its direction depended on the luminance of the intermediate sector: negative for a dark gray (43 of 50 pretrained networks) and positive for a light gray (40 of 50), and the same signs appeared in 14 networks trained from scratch (12/14 and 13/14). As in human observers, the response to four-level patterns followed from the difference between responses to their three-level components (mean held-out $R^2=0.90$), and this rule held within each network even though the component responses differed between networks. The response was about three orders of magnitude smaller than that to physical rotation, varied with stimulus phase, was not restricted to MIDD patterns, and depended on the learned pairing of network and decoder. A circuit model built from the fly connectome and a generic motion task thus acquires a structured response to static patterns that shares the luminance-dependent reversal and the summation rule described for human illusory motion.

## Introduction

Some stationary images appear to move. In the Fraser–Wilcox family of illusions, of which Kitaoka's "Rotating Snakes" is the best-known example, a repeating sequence of luminance steps produces a steady drift in a direction set by the order of the steps [@KitaokaAshida2003; @Conway2005; @BackusOruc2005]. Because nothing in the image moves, these patterns expose how motion signals are computed from spatial structure.

Two earlier studies frame the present work. First, a deep network trained only to predict the next frame of natural videos (PredNet) produced rotational motion for Rotating Snakes images that it had never seen, in the direction that humans perceive [@WatanabeEtAl2018IllusoryMotion]. Illusory motion can therefore arise as a by-product of learning about real motion; later work found that this output varies between trained instances of the same architecture [@KirubeswaranStorrs2023InconsistentMotion]. Second, human psychophysics with motion illusion-like discrete design (MIDD) disks, which reduce the illusion to three or four luminance levels repeated around a ring, established two regularities [@KobayashiWatanabe2023MIDD]. The perceived direction of a three-level pattern reverses as the intermediate luminance goes from dark to light, and the perceived velocity of a four-level pattern is predicted by the difference between the velocities of its two three-level components. The amount of illusion and the luminance at which the direction reversed differed between observers, whereas the summation rule held for all of them.

The fly offers a way to ask where such signals come from at the level of an identified circuit. Flies turn in response to static illusion patterns much as humans perceive them to move, and this behavior depends on the direction-selective T4 and T5 neurons [@AgrochaoEtAl2020IllusoryMotionFlies]. The pathway from photoreceptors to T4/T5 is mapped cell type by cell type and synapse by synapse [@MaisakEtAl2013DirectionMap; @StrotherEtAl2017DirectionalSelectivity], flies and humans share motion-estimation strategies [@ClarkEtAl2014MotionStrategy], and ON/OFF asymmetries in this pathway are tuned to the statistics of natural scenes [@FitzgeraldEtAl2011StimulusStatistics; @LeonhardtEtAl2016ONOFF].

FlyVis turns this anatomy into a trainable model [@LappalainenEtAl2024FlyVis]. Its recurrent network has the cell types and connectivity of the fly optic lobe, and its free parameters are fitted end-to-end so that a decoder can estimate optic flow from rendered Sintel movies. No neural recordings are used in training, yet the ensemble median predicted the measured ON/OFF preference of all 32 cell types for which it is known, and the networks recovered ON-motion selectivity in T4, OFF-motion selectivity in T5, and the absence of direction selectivity in nine of their input cell types; some predictions failed, including a reversed Tm4 response [@LappalainenEtAl2024FlyVis]. In the animal, T4/T5 signals are pooled by wide-field lobula-plate tangential cells [@BorstEgelhaaf1989MotionDetection]; in FlyVis this stage is replaced by a learned two-layer convolutional decoder that maps instantaneous network activity to a flow field. Because the decoder sees only the current activity, the comparison across time that motion estimation requires is carried out in the recurrent network. Fifty independently trained networks share the same wiring, so differences among them reflect the learned parameters alone.

Here we present the MIDD disks of the human study to FlyVis and measure the decoded flow. We ask three questions. Does a network constrained by the fly connectome and trained only on optic flow acquire a response to static illusion patterns? Does that response show the two regularities found in humans, the luminance-dependent reversal and the summation rule? And what makes its sign and size differ between networks that share one wiring diagram? Decoded flow is the output of a model; we use it to study the computation, and we do not treat it as a measurement of what a fly or a person perceives.

## Results

### Measuring the response to a static pattern
<!-- figure: 1 -->

A three-level MIDD (3MIDD) repeats the sectors black, intermediate gray of luminance $C$, and white 24 times around a ring; a four-level MIDD (4MIDD) repeats black, $C_1$, white, $C_2$ (Fig. 1A). Each pattern has a Mirror version in which the order of the sectors is reversed. We showed each disk as a stationary 1-s movie to the 50 pretrained FlyVis networks and averaged the decoded flow over the last 0.8 s.

The decoded flow for a static disk was dominated by a spatial pattern that was the same for the Original and Mirror versions and therefore carries no information about the order of the sectors. We removed it by taking half the difference between the two fields. What remains is the component that reverses when the pattern is mirrored, and it was rotational (Fig. 1C). We summarize it by the scalar $A=(T_O-T_M)/2$, where $T$ is the mean tangential (clockwise-positive) component of the flow over the ring, and summarize the shared part by $S=(T_O+T_M)/2$. $A$ is our measure of the illusory-motion signal.

Two reference points give the scale. A physically rotating propeller was decoded with the correct sign in 50 of 50 networks (Fig. 1B; Supplementary Fig. S1), with a mean tangential flow of about 9 for clockwise rotation. For the static 3MIDD with $C=48$, mean $|A|$ was 0.0105, about one thousandth of the response to real rotation and a median of 3.4% of the mean flow magnitude evoked by the static disk itself. The signal is small, as the percept is in humans, but its sign is systematic, as shown next.

### The response emerges during optic-flow training
<!-- figure: 2 -->

If the response were a property of the wiring alone it would be present before training. We trained 14 networks from scratch and evaluated every saved checkpoint (Fig. 2A–C). At initialization, $|A|$ was below $3\times10^{-9}$ for every network and every stimulus (Fig. 2E). It rose as the Sintel endpoint error fell, and by 100,000 steps the median $|A|$, normalized by the mean flow magnitude, was 0.038 for $C=48$, 0.035 for $C=207$, and 0.024 for the 4MIDD with $C_1=85$ and $C_2=170$. No MIDD or other illusion pattern was part of the training data. The response is therefore learned, and it is learned from a task that contains only real motion, as in the video-prediction network of @WatanabeEtAl2018IllusoryMotion, here with a different architecture and a different objective.

The sign of the learned response was reproducible. At 100,000 steps $A$ was negative in 12 of 14 networks for $C=48$ and positive in 13 of 14 for $C=207$ (two-sided binomial $p=0.013$ and $0.0018$; Bonferroni-adjusted $p=0.039$ and $0.0055$), and these majorities held at every checkpoint from 90,000 to 100,000 steps (Fig. 2C–D). For the 4MIDD, 11 of 14 networks were positive ($p=0.057$, adjusted $0.17$). Responses to other static images grew over the same period (Supplementary Fig. S8), a point we return to below.

### The direction depends on the intermediate luminance
<!-- figure: 3 -->

In the 50 pretrained networks we varied the intermediate luminance of the 3MIDD over 15 levels (Fig. 3A–B). The mean response was negative for $C=16$–112 and positive for $C=128$–239: the decoded rotation reversed as the intermediate sector went from dark to light. At $C=48$, $A$ was negative in 43 of 50 networks (mean −0.0093), and at $C=207$ it was positive in 40 of 50 (mean +0.0083; Fig. 1E). Thirty-four networks showed both signs in this order and one showed the opposite order (Fig. 3C). Within networks, $A$ increased with $C$ (median Spearman $\rho=0.69$; positive in 44 of 50). In 31 networks $A$ crossed zero exactly once, at a luminance that differed from network to network (mean $C=130$, s.d. 44).

Human observers show the same form of dependence: the perceived rotation of a three-level MIDD is strongly correlated with the intermediate luminance and reverses at a luminance that differs between observers [@KobayashiWatanabe2023MIDD]. The polarity differs. For a dark intermediate sector the human percept runs from black through gray to white, whereas the decoded flow runs from white through gray to black, and conversely for a light sector.

### Four-level responses follow from three-level responses
<!-- figure: 4 -->

In humans, the perceived velocity of a four-level MIDD equals the difference between the velocities of the two three-level MIDDs that it combines [@KobayashiWatanabe2023MIDD]. We tested the same rule on the decoded flow,

$$
A_4(C_1,C_2)\approx \alpha\,[A_3(C_1)-A_3(C_2)]+\beta ,
$$

in ten networks, for all 21 pairs of seven luminances, using a rendering in which the disk covers eight adjoining visual fields (Fig. 4A–C). The three-level difference accounted for most of the variance in the four-level response (mean $R^2=0.93$ across networks), and its sign matched the observed sign in 96.5% of pairs. The mean slope was 0.83, with a small offset of 0.0074 in magnitude, so the relation is close to, but not exactly, a plain difference. When all pairs containing one luminance were held out, the rule fitted on the remaining pairs predicted them with mean $R^2=0.90$ (95% CI 0.86–0.94; Fig. 4D; Supplementary Fig. S7).

The rule was shared, but its inputs were not. Each network's four-level responses were predicted well by its own three-level responses, and much less well by the mean three-level curve of the other nine networks (mean held-out $R^2=0.54$), by another single network's curve (0.34), or by the luminance difference $C_1-C_2$ alone (0.18; all three comparisons Holm-adjusted $p=0.006$; Fig. 4E). This mirrors the human data, in which the size of the illusion and the reversal point were individual while the summation rule was common.

The rule concerns the scalar $A$ and was strong in the eight-field rendering. In a seven-field comparison it remained strong at higher sampling resolution (mean $R^2=0.93$) and was weaker at the native resolution of a single eye model (0.44; Supplementary Fig. S2), which indicates that how finely the ring is sampled by the receptor lattice matters for composition.

A classical account of this illusion family is that a compressive nonlinearity applied to local motion-detector outputs before spatial pooling leaves a residual that does not cancel in an asymmetric pattern [@BachAtalaGerard2020RotatingSnakes]. An array of Reichardt detectors behaved accordingly: with linear pooling its output for static MIDD was near zero, and with the saturating nonlinearity it was directional, with the same net tangential direction as FlyVis for the two reference patterns and the same ordering of magnitudes (3MIDD larger than 4MIDD; Supplementary Fig. S4). Over a 21 × 21 grid of 4MIDD luminances, the mirror-reversing parts of the array output and of one FlyVis network were correlated ($r=0.46$) and agreed in sign at 81% of the 326 grid points at which both were reliably different from zero. A simple nonlinear detector array thus reproduces part of the structure of the FlyVis response, and the remainder shows that the trained network is not reducible to it.

### Sign and magnitude vary with phase and across networks
<!-- figure: 5 -->

Rotating the disk by a fraction of one sector period changes which receptors fall on which sectors. Across twelve such phases for $C=48$, networks kept their relative ordering (absolute-agreement ICC(A,1) = 0.76; Fig. 5A–B), and the value at the reference phase tracked the phase average ($r=0.88$; same sign in 39 of 50 networks). The magnitude nevertheless depended on phase: the phase-averaged mean was −0.0038 compared with −0.0093 at the reference phase, 34 networks changed sign at one or more phases, and the phase-averaged $A$ was negative in 32 of 50. Small shifts of the disk and restriction to the outer receptors, where the sectors are sampled most finely, changed $A$ and $S$ as well (Fig. 5C–E; Supplementary Figs. S5, S6). The coarse hexagonal lattice of the model eye, about 31 receptors across a disk of 72 sectors, is thus a major source of variation, and values at the reference phase (Figs. 1–3) should be read with this in mind.

Whether the Original and Mirror disks give flows of opposite sign depends on both components: the raw signs differ exactly when $|A|>|S|$. This was the case in 21 of 50 networks at $C=48$, 18 of 50 at $C=207$, and 12 of 50 for the 4MIDD (Fig. 1D; Fig. 3D). In the remaining networks the shared component was the larger one, and the direction-dependent signal rode on top of it.

Differences between networks were not explained by how well they solved the training task. Sintel endpoint error was weakly related to signed $A$ ($\rho=0.28$), to $|A|$ ($\rho=-0.22$), and to phase variability ($\rho=-0.33$); none of the three associations remained below 0.05 after Holm correction (adjusted $p=0.09$, $0.13$ and $0.06$). A link to the learned circuit solution is suggested by T4c tuning, which @LappalainenEtAl2024FlyVis showed to fall into distinct clusters across networks. Phase-averaged $A$ at $C=48$ was −0.0077 in the 31 networks with upward-selective T4c, as in the fly, and +0.0027 and +0.0026 in the 7 downward-selective and 12 untuned networks (permutation $p=0.018$, Holm-adjusted $p=0.053$; Fig. 5F; Supplementary Table S5A).

### Static structure in general evokes decoded motion

The response was not confined to the MIDD arrangement. When the sectors of each disk were shuffled while preserving its luminance histogram, the mirror-dependent component was as large as or larger than for the ordered disk (mean magnitude, ordered versus shuffled: 0.0106 versus 0.0133 at $C=48$, 0.0094 versus 0.0126 at $C=207$, and 0.0034 versus 0.0117 for the 4MIDD; Fig. 3F; Supplementary Fig. S5). Balanced disks, in which each transition occurs equally often in both directions (Fig. 3E), random-pixel images, and uniform gray fields also gave nonzero tangential flow. The responses to shuffled, balanced, and uniform images developed during training along with the MIDD response (Supplementary Fig. S8). Varying the number of sectors showed that the standard 72 and 96 sectors were not the optimum in any of ten networks; the response changed with spatial frequency and sampling (Supplementary Fig. S6).

Optic-flow training therefore makes the network and its decoder responsive to static spatial structure of many kinds. What distinguishes the ordered MIDD is not the size of its response but its regularity: a sign that follows the intermediate luminance across independently trained networks, and a four-level response that can be computed from three-level ones.

### The response depends on motion pathways and on the learned readout
<!-- figure: 6 -->

To ask which signals the decoded response relies on, we replaced the activity of selected cell types at the decoder input with their activity for a uniform gray field, leaving the recurrent network untouched (Fig. 6A–C; Supplementary Fig. S9). In ten networks, replacing T4, or T4 and T5 together, shifted the $C=48$ response by +0.054 (95% CI 0.014–0.100) and +0.067 (0.031–0.110) of the mean flow magnitude. The same replacement changed the decoded response to a rotating propeller and to moving edges. The static-pattern response thus passes through the same T4/T5 channels as real motion, in line with the dependence of the fly's behavioral response on these neurons [@AgrochaoEtAl2020IllusoryMotionFlies].

Finally, we paired each of ten networks with the decoder of every other (Fig. 6A, D–E; Supplementary Fig. S10). Matched pairs decoded both directions of a drifting grating correctly in 10 of 10 cases; mismatched pairs did so in 9 of 90, and their static response was larger (mean $|A|$ 0.028 versus 0.009 for matched pairs). Each decoder is thus adapted to its own network, and the decoded response to a static pattern is a property of the trained pair.

## Discussion

A network with the wiring of the fly visual system, trained only to estimate optic flow in rendered movies, acquired a direction-dependent response to static illusion patterns. The response was absent at initialization, appeared during training without any illusion pattern in the training data, took a sign set by the intermediate luminance in most independently trained networks, and combined across luminance levels by a difference rule. These are the properties that characterize the human percept of the same patterns [@KobayashiWatanabe2023MIDD], apart from polarity.

### Illusory motion as a by-product of learning to see motion

@WatanabeEtAl2018IllusoryMotion found that a network trained to predict video frames reproduced illusory rotation and proposed that the illusion follows from learning the regularities of real motion. The present result extends this observation along two dimensions. The objective is different, supervised flow estimation in place of frame prediction, and the architecture is a connectome with identified cell types in place of a generic convolutional hierarchy. That a static-pattern response appears in both cases suggests that it is a common consequence of fitting motion-sensitive circuitry to natural image sequences. The nonlinear detector array points to one way in which this can happen [@BachAtalaGerard2020RotatingSnakes]: a system tuned to natural scenes need not be linear, and a nonlinearity ahead of spatial pooling turns an asymmetric static pattern into a net directional signal. ON/OFF asymmetries of the kind that improve velocity estimation in natural scenes are a candidate source of such nonlinearity in the fly pathway [@FitzgeraldEtAl2011StimulusStatistics; @LeonhardtEtAl2016ONOFF].

### A shared rule with individual parameters

The human data separated two levels: local motion signals whose strength and reversal point differ between observers, and an integration stage that sums them in the same way in everyone [@KobayashiWatanabe2023MIDD]. The model shows the same separation. The three-level response curve was specific to each network, to the extent that another network's curve was a poor predictor, whereas the difference rule held in every network tested. In FlyVis the fifty networks share one connectome, so the individual part must come from the learned parameters. Fixing the wiring and the task does not fix the solution, as @LappalainenEtAl2024FlyVis showed for the tuning of T4c and as has been described for machine-learning models in general [@DAmourEtAl2022Underspecification]. The tendency of networks with fly-like T4c tuning to share one sign of the response suggests that this variation is structured by the circuit solution a network has found, a relationship that could be tested directly with the cell-type response properties of the fifty networks.

### What the fly model adds

Because every unit in FlyVis corresponds to a cell type, the response can be related to circuit elements. It depended on T4 and T5 activity at the decoder input, the neurons that carry the fly's behavioral response to static illusions [@AgrochaoEtAl2020IllusoryMotionFlies]. It also depended on the readout: decoders were not interchangeable between networks. In the fly, the corresponding readout is performed by lobula-plate tangential cells with fixed, wide receptive fields [@BorstEgelhaaf1989MotionDetection], and replacing the learned decoder with a tangential-cell-like pooling of T4/T5 activity would be a natural next step toward a comparison with behavior.

### Limitations

Decoded flow is a model output and we did not compare it quantitatively with fly behavior or with new human measurements; the comparison with human data concerns the form of the dependence on luminance and the summation rule. The response is small relative to that for physical motion, it is sensitive to the phase and placement of the disk on the coarse receptor lattice, and its polarity is opposite to the human percept. It is not specific to MIDD: other static images, including shuffled ones, evoke responses of similar or greater magnitude. The summation rule was established for the scalar $A$ in an eight-field rendering and was weaker at the native resolution of a single eye model. We did not train networks without the connectome constraint, so we cannot say which properties depend on it. The interventions replace activity at the decoder input in a model and are not equivalent to silencing neurons in an animal, and the detector array is a partial computational analogy.

## Methods

### Model and networks

We used the connectome-constrained recurrent networks of FlyVis and their optic-flow decoders [@LappalainenEtAl2024FlyVis], with FlyVis v1.2.0 (commit `92b3845cc426dd309a1a0e1b3890156c42e14021`). The pretrained networks were obtained with `flyvis download-pretrained`.

Three sets of networks were used. (i) The 50 pretrained networks of the FlyVis ensemble (`flow/0000/000`–`049`) were used for Figs. 1, 3 and 5A–B, for the static controls, for the comparison with task error, and for the propeller calibration. Subsets of ten of them were used where stated: networks 000–009 for the summation rule (Fig. 4), for phase analyses of the other two reference patterns, for placement, radial and sector-count analyses, and for decoder-input replacement (Fig. 6B–C); networks 000, 005, …, 045 for the exchange of decoders (Fig. 6D–E). (ii) Fourteen networks were trained from scratch for this study (seeds 000–013; Fig. 2). (iii) Silencing inside the recurrent network used six of the networks trained from scratch at step 250,000 (seeds 001, 002, 003 and 010, with 002 as a hold-out, and seeds 000 and 008 for comparison). Identical numbers in different sets do not denote the same network. The sets and the conditions of each analysis are listed in Table S1.

### Stimuli

A 3MIDD has 72 sectors of equal angle: the Original repeats the luminances [0, C, 255] 24 times in the clockwise direction and the Mirror repeats [255, C, 0]. A balanced 3MIDD repeats [0, C, 0, 255, C, 255] 12 times. A 4MIDD has 96 sectors: the Original repeats [0, C1, 255, C2] 24 times, the Mirror repeats [0, C2, 255, C1], and the balanced pattern repeats [0, C1, 255, C2, 0, C2, 255, C1] 12 times. Mirror therefore denotes a reversal of the spatial order of the luminances, not an inversion of contrast. In the balanced patterns every luminance transition occurs equally often in both directions; they are analysed as stimuli in their own right. Patterns are generated by `src/flyvis_midd/stimuli.py`.

Images are 382 × 382 pixels, with an inner and outer ring diameter of 55 and 382 pixels as in the human study [@KobayashiWatanabe2023MIDD], white outside the ring, at phase 0° unless stated. Integer luminances are divided by 255. The three reference patterns are 3MIDD with C = 48 and C = 207 and 4MIDD with C1 = 85 and C2 = 170. The luminance series (Fig. 3) uses C = 16, 32, 48, 64, 80, 96, 112, 128, 143, 159, 175, 191, 207, 223 and 239.

The propeller (Fig. 1B; Supplementary Fig. S1) has three blades and is shown stationary, rotating clockwise, or rotating counterclockwise at 1 Hz, as 128 × 128-pixel images.

### Rendering and presentation

In the single-eye rendering, the image is sampled by the FlyVis eye model `BoxEye(extent=15, kernel_size=13)`: 721 receptors on a hexagonal lattice, each averaging a 13 × 13-pixel patch with zero padding. All analyses use this rendering unless stated.

The summation rule (Fig. 4) uses an eight-field rendering, in which the image is centred on a black 3:2 canvas spanning eight adjoining fields arranged in rows of 3, 2 and 3 with row offsets [0, 1, 0]; the canvas is resized bilinearly (`align_corners=False`) to fit the layout. Decoded vectors at coincident positions are averaged within each frame after rounding coordinates to eight decimals. The comparison of renderings (Supplementary Fig. S2) uses a seven-field layout at the native resolution and at a higher resolution (`highres_232`); results are reported separately for each rendering.

Every stimulus is a movie of 50 frames at 50 Hz (dt = 0.02 s); a static stimulus repeats one image. Before each movie the network state is brought to steady state for 1 s on the first frame (`network.fade_in_state`), and these frames are not recorded. Networks and decoders are in evaluation mode without gradients, on CPU in single precision (`run_flow_inference` in `src/flyvis_midd/flow.py`). The decoder returns a flow vector (u, v) at each receptor and frame. All measures use frames 10–49. The flow fields in Fig. 1B–C are the decoder output averaged over these frames and over the 50 pretrained networks; for the static patterns the half-difference between the Original and Mirror fields is shown, and the mean tangential component of that field over the analysis ring equals A.

### Tangential flow and the components A and S

Receptor positions are in image coordinates, with x rightward and y downward, and the decoder vector is converted once as (u, v) → (u, −v). For a receptor displaced by (dx, dy) from the mean receptor position, at radius r, the clockwise unit tangent is (−dy/r, dx/r). The analysis ring comprises receptors with 0.14 r_max ≤ r ≤ 0.98 r_max (698 receptors). T is the mean, over these receptors and frames 10–49, of the projection of the flow on the tangent; positive T is clockwise. G is the mean Euclidean magnitude of the flow over the same receptors and frames. Both are in the units of the decoder output (`image_rotation_flow_metrics` in `src/flyvis_midd/rotation.py`).

For each network, pattern and condition, A = (T_O − T_M)/2 and S = (T_O + T_M)/2, where T_O and T_M are the values for Original and Mirror. T_O and T_M have opposite signs exactly when |A| > |S|. The balanced pattern does not enter these definitions. Where A is expressed relative to flow magnitude, it is divided by the mean of G for Original and Mirror.

In the eight-field rendering, T is computed with the tangent (dy/r, −dx/r) over the ring 0.14–0.98 of the image radius centred on the placed image, so that the stored scalars are counterclockwise-positive; a rotating propeller rendered in the same way gave negative values for clockwise and positive values for counterclockwise rotation in all ten networks (Supplementary Fig. S1E). In Fig. 4 these scalars are negated so that all figures are clockwise-positive.

For the propeller, the direction is counted as correct when T/G is positive for clockwise and negative for counterclockwise rotation. Rotation is counted as detected when, in addition, the smaller |T/G| of the two directions exceeds 0.1 and the smaller ratio of G for the moving propeller to G for the stationary propeller exceeds 3.

### Static controls

Sector-shuffled disks were made by permuting the luminances among the sectors, which preserves the histogram of the sectors and of the image; ten shuffles were drawn for each pattern (seed 2026100301). For ordered and shuffled disks alike, the mirror-reversing component was computed from the image and its left–right reflection, and the ten shuffles were averaged within each network. Differences between ordered and shuffled disks are summarized across networks with 10,000 bootstrap resamples of networks (seed 2026100504). Further controls were images of random pixels with the luminance histogram of the pattern, a uniform gray field of luminance 128, and the propeller at 382 × 382 pixels. For a uniform field only T and G are defined.

### Summation rule

For each of the ten networks, A3(C) was measured for seven luminances (48, 80, 112, 143, 175, 191 and 207) and A4(C1, C2) for the 21 pairs with C1 < C2. Within each network, A4 was regressed on A3(C1) − A3(C2) by ordinary least squares with an intercept, and $R^2=1-\Sigma(y-\hat y)^2/\Sigma(y-\bar y)^2$. Sign agreement compares the sign of A3(C1) − A3(C2), without fitting, with the sign of A4, for pairs in which |A3(C1) − A3(C2)| is at least 5% of the range of A3 in that network (18–21 pairs per network). All summaries are computed within networks and then averaged across networks.

For held-out prediction, all pairs containing one luminance were removed, slope and intercept were fitted on the remaining pairs, and the removed pairs were predicted; the measured A3 at the held-out luminance was used to form the prediction. Each pair is predicted in two folds, giving 42 predictions per network. Leaving out single pairs gave similar results (Table S6).

The same procedure was applied with other predictors in place of the network's own A3 difference: the mean A3 curve of the nine other networks, the A3 curve of each of the nine other networks individually (averaged within the target network before comparison), and C1 − C2. Differences in mean held-out $R^2$ were assessed with 10,000 bootstrap resamples of networks and an exact paired sign-flip test over the $2^{10}$ sign assignments, with Holm adjustment across the three comparisons (seed 2026100502). As further references (Supplementary Fig. S7F), the A3 values were replaced by random smooth antisymmetric functions B(C1) − B(C2), with B drawn from a Gaussian process with a squared-exponential kernel (length scale 0.25, and 0.1 and 0.5 as alternatives), centred and scaled to the root-mean-square of A3 in each network; 2,000 draws were used (seed 2026100305), with rank-based p values and Holm adjustment.

### Phase, placement, sampling, and sector count

The phase analysis rotated the 3MIDD with C = 48 to twelve equally spaced phases covering one 15° period of the pattern (steps of 1.25°) in all 50 pretrained networks; the other two reference patterns were tested in networks 000–009. ICC(A,1) is the single-measure, absolute-agreement intraclass correlation computed on the network × phase matrix of A, with intervals from 10,000 bootstrap resamples of networks.

Placement was tested by shifting the disk by 3 pixels in either direction along the horizontal or the vertical image axis, with white fill and no interpolation, keeping the analysis ring fixed (networks 000–009). The change in A and in S relative to the unshifted disk was divided by G.

For the radial analysis, the spacing between each receptor and its nearest neighbour was computed from the receptor positions, and the arc length of one pattern period at radius r is 2πr/24. A, S and G were recomputed from the stored flow in seven radial bins and in the outer ring, defined as the receptors at which one period spans at least two receptor spacings (532 of the 698 receptors).

The number of sectors was varied over 36, 48, 60, 72, 84, 96 and 120 for 3MIDD and 32, 48, 64, 72, 80, 96 and 120 for 4MIDD, at two phases (0 and half of one unit), in ten networks (008, 009 and 005, fixed first, then 000–004, 006 and 007). The image size, ring and luminances were unchanged, so that the density of edges varies with the number of sectors.

### Networks trained from scratch

Checkpoints were saved every 1,000 steps. The archive contains 2,586 files: 2,567 regular checkpoints, including step 0, and 19 irregular ones that were not used. All fourteen networks have checkpoints up to step 100,000, and the analyses in the main text use steps 0–100,000. A, S and G were computed at every checkpoint. The step at which the response appears (Supplementary Fig. S8A–B) was evaluated for thresholds of |A| of 0.0005, 0.001, 0.002 and 0.005, as the first checkpoint above threshold and as the first of three consecutive checkpoints above threshold; networks that do not cross are counted as such and medians refer to those that cross. Sign counts at step 100,000 were compared with a probability of 0.5 by exact two-sided binomial tests, with Bonferroni adjustment across the three patterns.

Sintel endpoint error was evaluated at each checkpoint on a fixed set of 15 samples (sequences 0, 5, 10, 15 and 22, three vertical splits each), without augmentation, with 19 frames resampled to 40 frames at dt = 0.02 s and a central crop of 0.7. These sequences were not held out from training, so the value tracks progress on the task and is not a test error.

Static controls during training (Supplementary Fig. S8E–F) were evaluated at steps 0, 10,000, 50,000 and 100,000 for 3MIDD C = 48, its balanced pattern, one shuffled disk, and the uniform field. Responses to the propeller and to moving edges (Supplementary Fig. S8G–H) were evaluated every 10,000 steps in three networks (seeds 000, 004 and 007) chosen before the evaluation.

### Task error of the pretrained networks

Endpoint error of the 50 pretrained networks was evaluated on the same 15 Sintel samples, after 0.5 s of steady-state preparation, as the mean endpoint error over 40 frames and 721 receptors. Its Spearman correlations with A at the reference phase, with |A|, and with the standard deviation of A across phases divided by G were computed with 10,000 bootstrap resamples of networks and Holm adjustment across the three.

### Replacement of activity at the decoder input

The decoder receives the activity of 34 cell types. In the main analysis (Fig. 6B–C; networks 000–009), the activity of selected cell types was replaced by their activity for a uniform gray field of luminance 0.5, matched in frame and receptor position; the recurrent network was not simulated again. The cell types replaced were T4a, T4b, all T4, all T4 and T5, Tm1 (as a control), and all inputs. We verified that replacing nothing reproduces the original output exactly and that channels not selected are unchanged. Stimuli were 3MIDD Original and Mirror at seven luminances (0, 48, 85, 128, 170, 207 and 255), the stationary and rotating propeller, and edges moving right and left. The measure is the change in the paired contrast (Original minus Mirror for MIDD at C = 48, clockwise minus counterclockwise for the propeller, right minus left for edges, each halved) caused by the replacement, divided by G without replacement. Intervals are from 10,000 bootstrap resamples of networks (seed 2026100502).

A second analysis (Supplementary Fig. S9C) replaced the activity by its mean over the 21 3MIDD conditions of the summation experiment (seven luminances × Original, Mirror and balanced) in the eight-field rendering. With x and y the vectors of A3 over the seven luminances without and with replacement, the gain is (y·x)/(x·x) and the loss of the response is 1 − gain. Mean losses are given with intervals from 50,000 bootstrap resamples of networks (seed 10012) and one-sided exact sign-flip tests; T4a was specified as the primary test, and Benjamini–Hochberg adjustment was applied within the other families of tests. The two analyses differ in baseline and stimuli and are not pooled.

The relation between activity and decoded flow (Supplementary Fig. S9B, G) was examined for the same 34 cell types in ten networks. The preferred direction of each cell type was obtained from responses to edges of intensity 0 and 1 moving in 12 directions (30° steps), leaving out the network under study. The activity measure is the Original-minus-Mirror half-difference of activity, weighted by the tangential component of the preferred direction and averaged over the ring and frames; it is normalized by its root-mean-square over the seven luminances and is retained when that value exceeds the largest corresponding value for the balanced patterns. Spearman correlations with A3 across the seven luminances were computed within networks, with Benjamini–Hochberg adjustment.

### Silencing within the recurrent network

In the six networks of set (iii), the activity of all T4c or all T4d cells was set to zero throughout the steady-state preparation and the stimulus (Supplementary Fig. S9D, H). As a reference, the same number of T4 cells was silenced at random positions, matched to the target within twelve angular sectors (199 random sets per network and target). The effect on A was averaged over twelve phases of 3MIDD C = 48. The effect on the task is the change in Sintel endpoint error on sequences 12, 13 and 16; sequences 2, 7 and 9, which had been used for calibration, were excluded.

### Exchange of decoders

Each of ten networks (000, 005, …, 045) was read out by each of the ten decoders, for 3MIDD C = 48 and for a horizontal grating of three spatial cycles drifting at one temporal cycle per second, contrast 0.35, rightward or leftward. The grating response is Q = (ū_right − ū_left)/2, and both directions are counted as correct when the mean u is positive for rightward and negative for leftward drift. For comparisons between a network's own decoder and the others, the nine other decoders were averaged within each network. The variation of A and of Q over the 10 × 10 table was divided into the parts attributable to network, to decoder and to their interaction by a two-way decomposition of the centred sum of squares (Supplementary Fig. S10C–D), with bootstrap intervals; because each pair is measured once, interaction and measurement error cannot be separated.

### Prolonged presentation

Three pretrained networks (024, 041 and 042), chosen as the 90th, 50th and 10th percentiles of |A| for 3MIDD C = 48, were shown the static disk for 500 frames (10 s) without resetting the state (Supplementary Fig. S3). The steady-state preparation lasted 0, 0.5, 1 or 2 s. In a further condition the image was displaced from frame to frame by up to 1 or 2 pixels along a fixed random path (seed 2026100414) that starts and ends at zero displacement. Windows of frames 10–49, 50–99, 200–249 and 450–499 were defined in advance.

### Detector array

The detector array (Supplementary Fig. S4) follows @BachAtalaGerard2020RotatingSnakes: local motion-detector outputs d are passed through the saturating function $f(d)=\sqrt{2}\,d/\sqrt{1+d^2}$ before spatial summation; without this function the summed output for static patterns is zero to numerical precision. The sign of the array output and of the FlyVis output (network 000, single-eye rendering) was fixed with physically rotating stimuli before static patterns were compared. For the 4MIDD luminance grid, C1 and C2 were varied in 21 steps each; the mirror-reversing and shared parts of each output were obtained by exchanging C1 and C2. Sign agreement was computed over the 326 grid points classed as robust in the stored analysis, and the correlation over all 441 points. These grid values describe one network and are not independent samples.

### T4c tuning

The assignment of the 50 pretrained networks to three clusters of T4c tuning (upward-selective, 31 networks; downward-selective, 7; untuned, 12) was taken from the clustering distributed with FlyVis [@LappalainenEtAl2024FlyVis]. Phase-averaged A for 3MIDD C = 48 was compared across clusters by a permutation F test (20,000 permutations), with Holm adjustment across three endpoints (Table S5A).

### Statistics and reproducibility

The unit of analysis is the network. Luminances, pairs, phases, positions and checkpoints are repeated measurements within networks and are summarized within each network before any comparison across networks. Figures show individual networks with means, or medians with interquartile ranges, as stated in the legends.

All figures are drawn from stored responses and summaries by `scripts/render_figures_v2.py`; no model inference is needed to reproduce them.

## Data and code availability

Code, processed data, figure scripts and the manuscript source are available at https://github.com/eijwat/flyvis-midd-we, a fork of the original project repository (https://github.com/poxsalop5029/flyvis-midd). All figures can be redrawn from the stored data without running the model (`scripts/render_figures_v2.py`; Table S4). FlyVis v1.2.0 (commit `92b3845cc426dd309a1a0e1b3890156c42e14021`) and the pretrained networks are distributed by the FlyVis project (`flyvis download-pretrained`). Checkpoints of the networks trained from scratch are in `data/checkpoints/learning_custom_checkpoints.zip`.

Supplementary Tables S1–S6 follow the supplementary figures. The flow fields of Fig. 1B–C are stored in `data/precomputed/fig01/fig1_flow_fields.npz`; they were recomputed with `scripts/generate_fig1_flow_fields.py`, and the tangential flow recomputed from them agrees with the stored network-level table to within $3\times10^{-7}$. Records for the analyses of T4c tuning, T4/T5 activity and ON/OFF currents are in `data/precomputed/supplementary/biological_constraints/`.

## Supplementary text

### Relation to circuit properties of the networks

**T4c tuning.** Phase-averaged A for 3MIDD C = 48 was compared across the three clusters of T4c tuning in the 50 pretrained networks. Mean A was −0.007707 in upward-selective networks (n = 31), +0.002674 in downward-selective networks (n = 7), and +0.002613 in untuned networks (n = 12). The difference between clusters was suggestive (eta-squared = 0.157, permutation p = 0.0176, Holm-adjusted p = 0.0528). The variability of A across phases and the occurrence of sign changes across phases did not differ between clusters (Holm-adjusted p = 0.684 and 0.301; Table S5A). This association is correlational.

**T4/T5 activity.** In the 50 pretrained networks, an equal-weight projection of T4 and T5 activity onto the tangential direction had a mean mirror-reversing component of +0.000141 (95% CI [−0.000677, +0.001055], Holm-adjusted p = 1.000). Across networks its correlation with decoded A was Spearman $\rho$ = 0.116 (95% CI [−0.193, 0.415], Holm-adjusted p = 1.000), and its sign agreed with that of A in 27 of 50 networks (Table S5B). A fixed, equally weighted readout of T4/T5 activity thus did not reproduce the decoded response. This concerns the tested readout only and does not show that T4/T5 activity carries no signal related to the pattern.

**ON and OFF input currents.** A summary of the mirror-reversing difference between ON-pathway and OFF-pathway source currents had a mean of 4.52 × 10⁻⁸ (95% CI [−1.12 × 10⁻⁷, 2.16 × 10⁻⁷], Holm-adjusted p = 1.000), a correlation with decoded A of Spearman $\rho$ = 0.065 (95% CI [−0.216, 0.341], Holm-adjusted p = 1.000), and the same sign as A in 26 of 50 networks (Table S5B). Among four secondary measures, the mirror-reversing component of the OFF-pathway current was negatively correlated with decoded A (Spearman $\rho$ = −0.357, Holm-adjusted p = 0.048 within that family); this is an exploratory, correlational observation.

## Figure legends

### Figure 1. Decoded flow for physical rotation and for static MIDD patterns

**A**, MIDD stimuli. A three-level MIDD (3MIDD) repeats black, an intermediate gray of luminance C, and white 24 times, clockwise in the Original; the Mirror reverses the order. A four-level MIDD (4MIDD) repeats black, C1, white, C2. **B**, A propeller rotating clockwise (left), the decoded flow (middle; arrows, drawn on the luminance sampled by the 721 receptors), and its tangential component at each receptor (right). **C**, Static 3MIDD with C = 48 and C = 207: half the difference between the flows decoded for Original and Mirror, which is the part of the flow for Original that reverses in Mirror, and its tangential component. The mean tangential component over the ring is A. Curved arrows give the net direction. B and C show the mean of the 50 pretrained networks over frames 10–49; arrow lengths and colour ranges are scaled within each panel. **D**, Mean tangential flow T for Original against Mirror, 3MIDD C = 48; filled symbols, networks in which the two have opposite signs. **E**, A for the three reference patterns; one point per network, bars show means. All panels use the native single-eye rendering and clockwise-positive flow.

### Figure 2. The response to static patterns emerges during optic-flow training

Fourteen networks trained from scratch, evaluated at every 1,000 steps up to 100,000; native single-eye rendering, clockwise-positive flow. **A**, Sintel endpoint error (median and interquartile range across networks). **B**, |A| divided by the mean flow magnitude evoked by the same disks (median and interquartile range). **C**, A during training for the three reference patterns; thin lines, individual networks; black, median. **D**, A at 100,000 steps; one point per network, bars show means. **E**, |A| at initialization (filled) and at 100,000 steps (open), on a logarithmic scale; lines connect the same network.

### Figure 3. Dependence on the intermediate luminance, and static controls

Fifty pretrained networks, native single-eye rendering, clockwise-positive flow. **A**, 3MIDD Originals at five of the 15 intermediate luminances tested (triangles in B). **B**, A against the intermediate luminance C; thin lines, individual networks. **C**, A at C = 207 against A at C = 48; filled symbols, networks with a negative value at C = 48 and a positive value at C = 207. **D**, T for Original against Mirror for the three reference patterns; filled symbols, opposite signs. **E**, T for balanced patterns, in which every luminance transition occurs equally often in both directions. **F**, Magnitude of the mirror-reversing component for ordered disks and for disks with shuffled sectors (mean of ten shuffles per network); lines connect the same network, bars show means.

### Figure 4. Four-level responses follow from three-level responses

Ten pretrained networks (000–009), eight-field rendering, seven intermediate luminances and their 21 pairs. Values are shown clockwise-positive; the stored eight-field scalars, which are counterclockwise-positive, were negated. **A**, The rule tested: the response to a four-level pattern is compared with the difference between the responses to the two three-level patterns that it combines. **B**, Three-level response against intermediate luminance; thin lines, individual networks. **C**, Observed four-level response against the three-level difference for all pairs and networks, with the line of equality and the mean of the per-network linear fits. **D**, R² of the fit in each network, and R² for pairs containing a held-out luminance. **E**, Held-out R² when the three-level responses are those of the same network, the mean of the other nine networks, a single other network (mean over the nine), or are replaced by the luminance difference. Lines connect the same network; bars show means.

### Figure 5. Dependence on phase, sampling, and the learned circuit solution

3MIDD C = 48, clockwise-positive flow. **A**, A at twelve rotations of the disk spanning one 15° period of the pattern, 50 pretrained networks. **B**, A at the reference phase against A averaged over the twelve phases; filled symbols, same sign. **C**, The 721 receptors of the model eye drawn on the disk; red, the outer ring in which one pattern period spans at least two receptor spacings. **D**, A computed over the whole analysis ring and over the outer ring (ten networks). **E**, Change in A and in S when the disk is shifted by 3 pixels, relative to the mean flow magnitude (ten networks, mean over shifts). **F**, Phase-averaged A in the 50 pretrained networks grouped by the tuning of their T4c cells (clusters of Lappalainen et al. 2024). Lines connect the same network; bars show means.

### Figure 6. The response depends on motion pathways and on the learned readout

**A**, The two interventions. **B**, Change in A for static 3MIDD C = 48 when the activity of T4, or of T4 and T5, at the decoder input is replaced by their activity for a uniform gray field, divided by the mean flow magnitude without replacement (ten networks, 000–009). **C**, The same measure for the clockwise-minus-counterclockwise response to a rotating propeller and the rightward-minus-leftward response to a moving edge. **D**, |A| for static 3MIDD C = 48 when each of ten networks (000, 005, …, 045) is read out by its own decoder or by the decoders of the other nine (mean). **E**, Network–decoder pairs that decode both directions of a drifting grating with the correct sign. Lines connect the same network; bars show means.

## Supplementary figure legends

### Supplementary Figure S1. Decoding of physical rotation

**A**, The three-bladed propeller, stationary and rotating in either direction (128 × 128 pixels, 50 frames at 50 Hz). **B**, Mean tangential flow T in the 50 pretrained networks; lines connect the same network. The direction was correct in 50 of 50 networks. **C**, The two criteria for detecting rotation (dashed lines); they were met in 49 of 50 networks. **D–E**, Stored rotation scalar for clockwise and counterclockwise rotation in networks 000–009, in the single-eye rendering (clockwise-positive) and in the eight-field rendering (counterclockwise-positive).

### Supplementary Figure S2. The summation rule in two renderings

Networks 000–009, seven-field layout at the native resolution and at a higher resolution. **A**, R² of the regression of the four-level response on the three-level difference. **B**, Fraction of pairs in which the sign of the three-level difference matches the sign of the four-level response. **C–D**, Four-level response against the three-level difference for network 000 in the two renderings; dashed, equality. **E–F**, Comparison of the whole four-level flow field with the difference between the two three-level fields: root-mean-square error relative to the prediction, and cosine similarity, averaged over the 21 pairs. Lines connect the same network; bars show means.

### Supplementary Figure S3. Prolonged static presentation

**A**, Mean A in the 50 pretrained networks during the 1-s movie. **B–D**, A, S, and T for Original (solid) and Mirror (dashed) in three networks (024, 041, 042) during 10 s of presentation of 3MIDD C = 48; shading, the last second. **E**, A in the first and the last second. **F**, A in the last second for four durations of the steady-state preparation. **G**, |A| in the last second when the image is displaced by up to 1 or 2 pixels from frame to frame. **H**, T in the last second for the balanced pattern and the uniform field. Values of A in the last second were −0.02707, +0.009925 and −0.001720.

### Supplementary Figure S4. Comparison with a nonlinear motion-detector array

Detector array after Bach and Atala-Gérard (2020) and FlyVis network 000 in the single-eye rendering. **A**, Output of the array for static 3MIDD and 4MIDD when detector outputs are summed directly and when the saturating function is applied before summation. **B**, Output for physical rotation, used to fix the sign of each model. **C**, Output for the static reference patterns, each normalized to its larger value. **D**, Mirror-reversing part of the output over a 21 × 21 grid of 4MIDD luminances, normalized to its maximum. **E**, Agreement between the array and FlyVis over the grid, for the raw output and for the mirror-reversing part; sign agreement is over the grid points classed as robust. **F**, Root-mean-square of the mirror-reversing and shared parts of the FlyVis output over the grid.

### Supplementary Figure S5. Static controls, phase, and task error

Fifty pretrained networks unless stated. **A**, |A| for the ordered disk minus the mean |A| of ten shuffled disks. **B**, Rank of the ordered disk among the ten shuffles. **C**, Paired contrast relative to flow magnitude for the ordered disk, shuffled disks, random-pixel images, and the rotating propeller (3MIDD C = 48). **D**, T relative to flow magnitude for the uniform field and the balanced pattern. **E**, S across phase in networks 000–009. **F**, Fraction of the twelve phases at which Original and Mirror gave opposite signs. **G–H**, Sintel endpoint error against A at the reference phase and against the variability of A across phases.

### Supplementary Figure S6. Dependence on the number of sectors

Ten pretrained networks; 3MIDD with 36–120 sectors and 4MIDD with 32–120 sectors, at two phases. Columns, the three reference luminance settings; rows, A, |A| relative to flow magnitude, and S. The horizontal axis is the arc length of one pattern period divided by the receptor spacing. Thin lines, individual networks; thick lines, means for the two phases.

### Supplementary Figure S7. Held-out prediction and comparison predictors

Networks 000–009, eight-field rendering; values in the stored, counterclockwise-positive sign. **A–C**, Held-out R², root-mean-square error, and fraction of correct signs when the three-level responses are those of the same network, the mean of the other networks, one other network, or are replaced by the luminance difference. **D–E**, Slope and intercept of the fit in each network. **F**, Difference in held-out R² between the network's own three-level responses and random smooth functions, for three length scales; intervals from bootstrap resampling of networks.

### Supplementary Figure S8. Development of responses during training

Fourteen networks trained from scratch. **A–B**, Number of networks in which |A| exceeds a threshold by step 100,000, and the median step at which it does so for three consecutive checkpoints. **C–D**, A and |A| − |S| during training; thin lines, individual networks; thick lines, medians. **E**, Paired contrast relative to flow magnitude for the ordered, shuffled and balanced 3MIDD C = 48 at four steps. **F**, T relative to flow magnitude for the uniform field. **G–H**, Response to the rotating propeller and to moving edges in three networks.

### Supplementary Figure S9. Controls for the interventions, and activity of T4 subtypes

**A**, Change in A when all decoder inputs, or Tm1 alone, are replaced by their activity for a uniform gray field (networks 000–009). **B**, Spearman correlation, within networks and across seven luminances, between the activity measure of each T4 subtype and decoded A. **C**, Loss of the response when activity is replaced by its mean over the 21 three-level conditions; means and 95% bootstrap intervals. **D**, Change in Sintel endpoint error when T4c or T4d is silenced in the recurrent network (filled) or when the same number of randomly chosen T4 cells is silenced (open); six networks trained from scratch. **E**, Fraction of the response that remains after each replacement. **F**, Mean flow magnitude without replacement. **G**, Activity measure of the T4 subtypes against luminance; thin lines, individual networks. **H**, Change in phase-averaged A for the silencing in D (circles, target; squares, mean of random sets).

### Supplementary Figure S10. Exchange of decoders between networks

Ten pretrained networks (000, 005, …, 045), each read out by each of the ten decoders. **A**, A for 3MIDD C = 48 for every pair. **B**, Response to a drifting grating for every pair. **C–D**, Share of the variation in A and in the grating response attributable to network, decoder, and their interaction, with bootstrap intervals. **E**, |A| with a network's own decoder and averaged over the other nine. **F**, Pairs in which both directions of the grating were decoded with the correct sign.

## References

::: {#refs}
:::
