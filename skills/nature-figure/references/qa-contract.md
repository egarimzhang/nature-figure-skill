# Figure QA contract

Use the selected backend exclusively for plotting and visual QA. Inspect exported SVG/PDF
and a raster preview, not only a successful script exit. These personal defaults are not
a statement of universal journal compliance; verify a specified submission's official guide.

## Observable checks

- Correct final physical canvas/plot dimensions; no independent panel scaling or tight crop.
- Arial regular/italic are available and actually used. SVG text nodes remain editable;
  no unannounced fallback fonts, outlined text, mismatched mathematical font or clipped labels.
- Axis labels/ticks 6 pt; ordinary labels 6 pt; lowercase panels 10 pt, bold, with baseline 1 mm above the frame top.
- Axis/tick strokes 0.75 pt and #000000; curves 1.125 pt. Full frames once per side.
- Point-line and legend markers 4.5 pt, edges 0.6 pt; dense spectral raw points are separate.
- Bar/group outer edges retain side margins; no arbitrary hard-coded temperature limits.
  Row and column frame gaps start at 14 and 16 mm, respectively including labels and legends; increase only
  for actual content.
- After major x ticks are set, no x minors when distinct data positions correspond one-to-one
  with them; otherwise one unlabelled short midpoint minor per interval on continuous
  linear x axes. No invented categorical midpoint ticks. Units use parentheses; physical symbols italic.
- Panel labels anchored to left/top frame at physical offsets and move with the axes.
  Row top/bottom alignment survives twin/colourbar fitting. A column has an ordinary or
  nominal right boundary; narrowed twins are never subsequent alignment references.
  Colourbar RIGHT BORDER matches that standard boundary, labels outside. Check individual
  artist boxes in shared gutters: union boxes may overlap only in genuinely empty areas.
  Actual labels/marks must not collide or escape canvas. Check near adjacent panel letters.
- Exact approved anchors, main curves, main/mid paired curves, main-to-mid ordinary bar gradients,
  outline peaks. Three/four stacks use literal main/mid/light or outline/main/mid/light.
  Two equal active primary categories; no silent on-request extension. When authorized, prefer
  the active scheme's on-request order; keep Primary 3/4 mutually exclusive. Primary keys are primary1/primary2/primary3/primary4, not auxiliary blue. Do not auto-create auxiliary four-level ladders.
  Check requested layer counts and do not add errors to a no-error stack.
- Ordinary bars use opaque top-main/bottom-mid gradients without outlines; peak gradients remain readable/translucent. Native SVG gradient stops;
  intentional raster intensity maps disclosed, with editable labels and matrix data.
- Plot limits include all observations/errors and meaningful zero baselines; bounded
  percentages do not silently clip overflow. Breaks/normalization/offsets are explicit.
- Bars with replicates show mean and sample SD only, with no individual dots; raw observations remain in source data. Neutral bar errors sit topmost. Point-line errors use family outline.
- Non-peak closed shapes use light faces/outline boundaries; peak-shaped spectral components retain gradients.
- Errors have correct definition/n and asymmetric form when provided. Stacked errors are
  derived from cumulative replicate sums or justified covariance, not summed SDs. Check
  an anti-correlated replicate example to expose incorrect propagation.
- Legends match identities/order and occupy clear space; no font shrinking to hide overflow.
- Source script/data/parameters reproduce figures without an installed-skill path dependency.

## Statistical and image integrity

Record n and replicate definition, centre statistic, spread/interval, calculation/test,
paired structure and exact comparisons as applicable. Do not invent errors for real data.
A synthetic demonstration must be labelled as such; synthetic XRD/XPS cannot establish
real chemical assignments, surface phases or mechanisms.

For microscopy/blots record raw source, crops, scale calibration, adjustments and reuse.
Preserve scientific image aspect and channels; global adjustments must be disclosed.

## Export bundle

Fixed-size SVG with editable text/native gradients; PDF; PNG preview; TIFF as needed.
PDF gradients may be vector strips rather than a single editable gradient object.
Raster maps may remain embedded raster objects; identify them and retain source matrices.
Use dpi 300 for preview and 600 for TIFF by default, subject to the actual export request.
