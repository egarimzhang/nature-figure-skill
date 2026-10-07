---
name: nature-figure
description: >-
  Submission-grade Nature/high-impact journal figure workflow for Python or R. Use whenever the user asks to create, revise, audit, or polish manuscript figures, multi-panel scientific plots, figures4papers-style matplotlib plots, or journal-ready SVG/PDF/TIFF outputs, especially for Nature-family or other high-impact journals. Before plotting, define the figure's conclusion, evidence logic, export needs, and review risks. Default to Python unless the user explicitly requests R. Use only the selected backend for figure generation, previewing, exporting, and QA. Supports matplotlib/seaborn and ggplot2/patchwork/ComplexHeatmap. Not for dashboards or Illustrator/Figma-first infographics.
---

# Nature Figure Making Skill

Create editable scientific figures from a clear evidence/figure contract. For style
previews, the contract is visual evaluation using explicitly labelled synthetic data;
do not invent a scientific conclusion. Preserve user-specified panels and comparisons.

## Backend and scope

Default to Python without asking the user to choose a backend. Use R only when the user
explicitly requests R. An existing explicit selection persists across revisions. Use that backend exclusively
for drawing, previewing, export and visual QA. Check its runtime/packages before drawing;
if unavailable, report the exact blocker instead of switching languages. Read
[backend-selection.md](references/backend-selection.md) only for a requested recommendation.

Before plotting, establish purpose, data provenance, panel roles, final dimensions,
error definitions and exports. Adapt the detail to the request: do not block an already
specified styling preview with irrelevant scientific questions. Independent figures
remain independent unless a composite was requested. Never alter scientific data for
visual balance; do not infer peak assignments, smoothing, fits or error definitions.

## Active personal defaults

Always read [layout-contract.md](references/layout-contract.md) and
[color-contract.md](references/color-contract.md). These override old examples/gallery
styling. This is the user's chemistry template, not a claim of universal Nature compliance.
Only a specified submission target warrants checking its current official requirements.

- Final-size three-panel reference: 180 mm total width; ordinary plot rectangles
  46 × 35.38 mm (1.3:1). Axis text 8 pt, annotations/legends 7.5 pt, panel letters
  12 pt; all Arial, with Arial Italic for physical symbols. No silent font substitution.
- Full frame, dark-grey axes/text, 0.75 pt axes, 1.125 pt curves, 4.5 pt point-line
  markers. Row and column frame-to-frame gaps start at 14 mm, including labels and legends;
  bar margins use outer edges. Axis titles
  write quantities followed by parenthesized units, such as `Current density (mA cm$^{-2}$)`.
  After setting major x ticks, omit x minor ticks when the distinct observed x positions
  correspond one-to-one with major ticks; otherwise use one unnumbered midpoint minor
  tick per interval. See layout-contract.md for log/categorical axes.
- Preserve the 8 pt axis-title size first. For a long title, try moving it within the
  panel envelope, wrapping it, or shortening tick numbers with a multiplier; shrink
  the title only if these do not yield a balanced layout. Keep plot frames aligned.
- Anchor panel letters to the plot's left/top frame with physical offsets, never
  to axis-title bounds. Ordinary grids align left axes; mixed layouts may adjust
  horizontal positions and widths for twins/colourbars while retaining row top/bottom
  alignment and visual balance. Establish a standard unshortened column boundary first;
  a narrowed twin frame never becomes the reference for further panels. Colourbar right
  borders align to the standard boundary, with tick text outside. Labels move with their axes.
- Choose one registered scheme: primary 1/2 (default), primary 1/3 yellow, or primary
  1/4 orange. Primary 3 and 4 are mutually exclusive. Use exact light/mid/main/outline
  anchors and the scheme-specific on-request order in color-contract.md. Main is the
  curve default; paired measurements use main/mid. Non-peak closed shapes use light
  faces and outline boundaries. Ordinary non-stacked bars use an opaque gradient from
  main at the top to mid at the bottom, without an outline; repeated observations appear
  only as their mean and defined SD, not individual dots. Fitted peak-shaped spectra
  retain their separate translucent gradients. Three-layer stacks
  use main/mid/light; four-layer stacks add outline below main. Cyan/blue/violet remain
  one-anchor auxiliaries. Never add a colour solely because more data rows exist.
- Bar error bars are neutral dark and topmost. Point-line error bars use family outline
  where overlap needs series identity. Keep readable grey references and explicit
  uncertainty semantics; do not invent SD for observations without replicates.

Python implementations are [publication_colors.py](scripts/publication_colors.py) and
[publication_style.py](scripts/publication_style.py). Read [api.md](references/api.md)
for signatures. Copy needed definitions into delivered scripts so outputs do not depend
on the installed skill path. Use the native-gradient SVG exporter on a fixed canvas.

For R, read [r-workflow.md](references/r-workflow.md); implement identical physical
parameters in R without invoking Python for rendering. Do not confuse ggplot's mm
line widths with points.

## Integrity, privacy and delivery

Preserve source observations, labels, units, fits and uncertainty definitions. Document
normalization, offsets and interpolation. Real data with no uncertainty do not acquire
invented error bars. Synthetic previews must be identified in the caption/source bundle.

Do not expose private attachment filenames, template paths or private-material provenance
in prose, legends or code comments. Link user-facing deliverables normally; disclose
private sources only when the user asks for that audit trail.

Validate with [qa-contract.md](references/qa-contract.md) before delivery. Inspect rendered
exports at final dimensions: text collisions, clipping, colour distinction, frame/label
alignment and readable error bars. Provide editable SVG/PDF, preview PNG and reproducible
source/data; TIFF when requested or appropriate. Keep a stable canvas and physical sizes.

## Supporting references

- [chart-types.md](references/chart-types.md): bars, stacked errors, paired lines, spectra,
  GC comparison, CV, XRD maps, special aspect ratios.
- [common-patterns.md](references/common-patterns.md): physical layout and twin-axis fitting.
- [tutorials.md](references/tutorials.md): maintained executable preview entry points.
- [figure-contract.md](references/figure-contract.md): scientific evidence/review risks.
- [design-theory.md](references/design-theory.md): design choices and exceptions.
- [r-template-index.md](references/r-template-index.md): private R templates, if supplied.
- [demos.md](references/demos.md) and [nature-2026-observations.md](references/nature-2026-observations.md):
  historical layout ideas only; their sizes, colours and typography are not defaults.
