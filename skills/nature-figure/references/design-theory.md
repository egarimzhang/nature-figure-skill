# Design decisions for the maintained template

The active numeric policy is in layout-contract.md; colour roles are in color-contract.md.
Use scientific relationships to choose the visual encoding; defaults are an editable
starting point and do not turn a style preview into a scientific claim.

The 180 mm reference is a final-size composite. Three 75 mm inner rectangles cannot fit
it. Maintain physical typography/strokes and solve margins/plot width at final size;
never separately rescale panels when composing. Dark-grey framing reduces visual weight
without weakening coloured traces. Full frames do not imply four sets of ticks.

Panel letters are geometric anchors to each left/top frame, not to variable text extents.
Ordinary grids can align left axes. Mixed axis/colourbar layouts instead balance complete
occupied envelopes with common row top/bottom boundaries. Intrinsic image/geometric aspect
and purposeful right-edge alignment can override exact cross-row columns. Establish
one unshortened standard boundary for a column; do not let a twin-axis accommodation
cascade into progressive narrowing of later panels. Colourbar borders follow that
standard boundary, with readable text outside it.

Colour identifies relationships: core categories are equal, paired shades represent
related measurements, ordered depths represent explicit sequences. Main is readable for
curves; mid softens blocks; outline provides spectral boundaries. Avoid decorative
encodings that look like unlabelled data. Preserve categorical and continuous semantics.

Error bars, source definitions, scale choices and integrity are part of figure design.
No undocumented fits, smoothing, offsets, per-trace normalization or truncated intervals.
Legibility is checked on rendered outputs at final dimensions, not only a zoomed screen.
Keep an editable source and SVG; verify target-journal requirements when actually preparing
that submission, while distinguishing them from these personal defaults.
