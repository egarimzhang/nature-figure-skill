# R workflow

Use R exclusively once selected, including preview and QA renders; never call Python
for an R drawing. Check R/packages early. If unavailable, report the exact blocker
and provide R source or installation options instead of a substitute backend.

Apply the same physical defaults in layout-contract.md and colour definitions in
color-contract.md. Transcribe the selected numeric colours into the delivered R script;
do not execute Python helpers for rendering. Verify Arial regular/italic with the R
font/device stack and report missing fonts rather than silently replacing them.

Use ggplot2/grid for basic plots, patchwork for composition, ComplexHeatmap when the
matrix structure warrants it, svglite/cairo_pdf for editable vectors, ragg for raster.
Only require packages needed by the actual task.

Typography: axis text/title 8 pt, ordinary text/legends 7.5 pt, panel letters 12 pt.
Axes/error strokes 0.75 pt, curves 1.125 pt. Point-line/legend markers have a 4.5 pt
physical size and 0.6 pt edge; translate to the selected R point-size convention rather
than assuming it matches Matplotlib. ggplot2 line widths use mm: convert using
1 pt = 25.4/72 mm (0.75 pt is about 0.2646 mm), rather than passing point numbers as
mm widths. Draw a complete panel border without duplicate axis strokes. Minor tick
rendering should explicitly match the installed ggplot2 capabilities: one unnumbered
midpoint tick, 1.5 pt length, no grid. Do not silently omit it.

Grid physical units or measured grob bounds provide fixed panel dimensions and letter
offsets. Do not use auto-tagging that anchors to varying title bounds. Solve twin/colourbar
occupied widths while keeping row top/bottom alignment. Start multirow frame gaps at
12 mm including labels. A narrowed twin is not a column reference: align a colourbar's
right border to the ordinary unshortened frame or nominal grid boundary. Labels sit
outside; check actual artist/grob bounds. Default colourbar width/gap/tick pad are
1.8 mm / 2 mm / 3 pt. Intrinsic image aspect is preserved. Derive bar side margins from
outer edges, not group centres (about 4.85 mm per side in the 46 mm three-bar example).

Use the same registered pair and exact anchors, with main/mid for paired curves.
Choose Primary 1/2, Primary 1/3 yellow or Primary 1/4 orange; Primary 3/4 never coexist.
Scheme-specific extensions require explicit instructions. Cyan/blue/violet retain single
anchors; derive their outlines/tints only for the current use. Three/four-
layer primary stacks use main/mid/light or outline/main/mid/light, with errors only
when requested and supported. Use distinct primary1/primary2/primary3/primary4 keys, not auxiliary blue.

Ordinary bars use solid light faces with outline borders; stacks remain solid component levels.
Spectral fills need stronger tint/alpha and outlines. For matched replicate stacks,
compute cumulative sums per replicate before SD/SEM. State error definitions/n.

Use spaced slash units and italic physical symbols with Arial glyphs. Export SVG/PDF
at exact canvas size; retain editable text and native gradients when the selected R
implementation supports them, otherwise disclose rasterized fills and keep adjustable
source. PNG/TIFF can use ragg at appropriate dpi. Reopen exports using R-side tooling
and check final-size legibility, clipping, alignment and font fidelity.

The Python helpers/preview are executed tests for Python only; do not claim they validate
R rendering. R-specific rendering must be tested when an R figure is actually requested.
