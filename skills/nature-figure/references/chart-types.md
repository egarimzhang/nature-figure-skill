# Chart-specific decisions

Apply [layout-contract.md](layout-contract.md) and [color-contract.md](color-contract.md)
first. User-requested chart types and panels are preserved.

## Bars, stacks, errors

Bars retain zero; bounded percentages normally 0–100. Use a main-at-top, mid-at-bottom
gradient without an outline for ordinary bars; stacks retain solid component levels. About 50–60% category spacing for
bar/group width; group gaps distinguish categories. Negative/horizontal gradients get
deeper away from baseline. Compute side margins from actual outer bar/group edges; see
layout-contract.md. Optional single-family three/four-layer and two-family six-layer recipes
are in color-contract.md. Value labels are opt-in, not mandatory for every bar. Never
conceal cropped bars or error endpoints.

Errors: stroke/cap 0.75 pt, capsize 1.8 pt, alpha 1. Neutral axis-grey on bars and topmost; family outline on multi-series curves where overlaps need identity. Repeated bar observations show only their mean and sample SD, with n stated and raw values retained in source data. Other error definitions require an explicit request. A stacked boundary's uncertainty
is uncertainty of a SUM, including covariance. Use matched replicate cumulative sums,
provided cumulative intervals or a justified covariance model. Never add segment SDs.
In style tests, disclose simulated replicates and demonstrate the calculation explicitly.

## Paired point-line curves

Use main + mid for two measurements of one object, supplemented by filled/open
markers or deliberate line styles. Normal line width 1.125 pt, marker size 4.5 pt and
edge 0.6 pt. Do not assign pale variants to unrelated categories. Raw samples, models
and references need visibly distinct grammar, not invented smoothing/fitting. Match
legend markers to the series size. Synthetic trend tests may emphasize different
trajectories; never alter real observations to separate trajectories. Dense spectral raw
points need their own size rather than inheriting the point-line default.

## Before/after GC

For an explicitly requested before/after comparison, use a readable grey reference
and a main-colour after trace on the same retention-time scale with documented vertical
offsets. The approved stacked comparison has no divider between the two traces. A
translucent rectangle spanning the same retention-time window across both traces
can highlight an emerging peak (second-primary main, alpha 0.35 is the approved starting point). Place it
behind data with no border. Choose peak window/offset from the actual data, not the
preview's 6.7 min peak or 1.18 offset. Do not invent peak identity or presence/absence.

## Dual-axis bar/line combination

For two specified metrics, a single-family bar series and a different single-family
point-line series are available. Selectivity/conversion are bounded percentages unless
otherwise specified. Use main for the line, main-to-mid gradients for bars, neutral axes,
clear metric/axis mapping, and matching 4.5 pt legend markers. Keep left/height and fit
right-axis text; never propagate this shortened frame as the column reference.

## XPS, Raman, XAS

Read provided domain requirements for axis direction, baseline, offsets, normalization
and component assignment. Use main/outline gradient fills with documented alpha for
fitted positive peaks; raw hollow points and neutral total/background. Overlap cannot
be the sole identifier. Scheme-specific on-request order is defined in color-contract.md. Raman families can
occupy vertically offset blocks with a grey separator (the approved two-family example
places primary 1 below primary 2); label offsets/temperatures and
preserve actual amplitudes or disclose normalization. Use no chemical assignments in
synthetic data unless explicitly presented as hypothetical.

## CV and temperature-programmed XRD

CV: preserve forward/reverse acquisition order. One-family ordered shades may encode
scan rate/cycle only with labels; keep a readable grey reference/control. Synthetic CV
is a schematic, not evidence of a mechanism or fitted electrochemical parameters.

Temperature-resolved XRD: measured intensity can be a map or offset spectra, with
explicit temperature scale and colourbar/offset convention. Preserve raw intensity
or state normalization; do not imply a surface-only probe or identify actual phases
without evidence. Synthetic phase I/II peak transfer is a visual test only, not a
material identification. Raster maps may be embedded in SVG while all text/axes stay
editable; export matrix/coordinate data. Respect real temperature sampling/resolution.

## Special plots

Heatmaps/images may require square cells or intrinsic image aspect. Geometric equal
scales, log axes, polar/radar coordinates and microscopy channels have semantic
constraints; the default 1.3:1 rectangle does not override them. Numeric intensity and
centred deviations use continuous scales, not arbitrary categorical colours. Distinct
histograms/distributions require stated binning/normalization and real observations.

## IR maps, PDOS, energy profiles and Nyquist

For an IR map, distinguish absolute intensity from a reference difference. A signed
map must name the reference potential and centre its colour scale at zero; the second
active primary may identify growth of the specified peak. Do not convert real spectra to differences
or assign peak identities without instruction. Colourbar alignment uses the ordinary
frame reference, as for XRD.

PDOS uses the supplied energy reference and density units. Upper/lower groups may be
vertically offset for display; document offsets, mark E−EF=0 and do not equate a lower
panel with negative density or spin-down unless that convention is supplied. Requested
filled groups use light faces and outline boundaries. Do not invent an electronic state
assignment from the illustrative data.

A reaction-energy profile is not by itself proof of a rate-controlling step. Highlight
the specified step using the second active primary; preserve state energies, transition-state barriers
and conditions. If using a toy profile, label the highlighted step as illustrative.
Nyquist plots label Z′ and −Z″ with impedance units and preserve the complex sign
convention. When comparing semicircle geometry, use equal physical scaling per ohm;
achieve this through compatible limits/frame geometry rather than distorting arcs.
Models and fitted values require provenance; a synthetic equivalent circuit is a
visual test, not a parameter fit to measurements.
