# Maintained preview entry points

Latest approved palette test (180 × 54.88 mm) uses three panels: two-primary-plus-orange
XPS, two objects with two main/mid measurements, and three bars each with four solid
outline/main/mid/light layers, 12 values and no error bars. Orange is explicitly enabled
only for this XPS recipe. This is synthetic visual QA, not a chemical assignment.

```bash
python scripts/preview_approved_palette.py OUTPUT_DIRECTORY
```

The script imports canonical helpers and uses small stable fixtures under
`../assets/approved-palette-data/`. It exports the figure and both literal role cards,
parameters and data; it does not install anything. A current PNG is shown in the README.
This four-layer/no-error recipe does not remove the separate cumulative-error examples.


The current synthetic chemistry reference is `../scripts/preview_template.py`, a compact
180 × 153.65 mm 3×3 layout: GC before/after with a second-primary emerging-peak window; four paired
point-lines; one-family three-layer annotated stacks with cumulative SD; three-colour
XPS (orange explicitly enabled for this fixed test); twin-axis selectivity bars/conversion line; two-family six-layer annotated stacks;
CV with grey reference; temperature-XRD map; blue-below/coral-above Raman with separator.
All data are simulated, peak/phase names are illustrative, and n=4 applies only to the
mock stack repeats. Fixtures under `../assets/preview-data/` keep this visual test stable.

```bash
python scripts/preview_template.py OUTPUT_DIRECTORY
```

This preview exercises 4.5 pt point-line/legend markers, edge-aware bar margins, 12 mm
row gaps, and colourbar-border alignment to the ordinary panel b rather than the narrowed
twin e. Common style/colour helpers are imported from adjacent scripts. Pass an output directory
outside the installation; without an argument the preview uses a relative template-preview
directory in the current working directory.

The supplemental five-colour test is retained:

```bash
python scripts/preview_palette.py OUTPUT_DIRECTORY
# Compatibility alias for that same five-colour test:
python scripts/preview_colors.py OUTPUT_DIRECTORY
```

It retains five-family role swatches and five-component XPS, with the explicit colour
extension limited to this fixed QA recipe (including orange in its b/f panels); it does not change the rule requiring user instruction
for orange/teal/auxiliary violet. Its typography/layout follow the same maintained helpers.

Deliver a standalone source by embedding the needed colour/style functions and providing
its adjacent source_data, not by exposing imports tied to an installed skill directory.
All previews export SVG/PDF/PNG/TIFF and numerical parameters/source data; the main preview
also records geometry/colour checks. Use api.md for actual experiments, never preview
arrays or placeholder scientific assignments. Historical atlases are structure references,
not maintained typography/colour/spacing defaults.
