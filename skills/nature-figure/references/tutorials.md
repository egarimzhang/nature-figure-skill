# Maintained preview entry points

All previews use simulated data, not experimental claims or chemical assignments. Use
an explicit output directory outside the installation. Shared helpers are imported from
adjacent scripts; deliver standalone figures by embedding those helpers with source_data.

## Current six-colour palette

```bash
python scripts/preview_six_colors.py OUTPUT_DIRECTORY
# Compatibility entry points for the same preview:
python scripts/preview_palette.py OUTPUT_DIRECTORY
python scripts/preview_colors.py OUTPUT_DIRECTORY
```

The current 120 × 95.9 mm abcd layout uses 39 × 31.2 mm frames: six-colour
XPS; two objects/two main-mid measurements; three bars/four primary levels/no errors;
two Raman families with six offset spectra each. Primary 3 plus the three one-anchor
auxiliaries are explicitly enabled in a, not automatically used elsewhere. Fixtures are in assets/six-colour-preview-data.
The README shows its PNG; the script also exports role cards, editable vectors and data.

## Electrochemistry nine-panel stress test

```bash
python scripts/preview_electrochemistry.py OUTPUT_DIRECTORY
```

a: potential-dependent signed IR reference difference and aligned colourbar; b: three-colour
XPS (Primary 3 explicitly requested); c: two paired objects; d: single closed CV loop with
outline/light fill; e: Primary 1/2 grouped gradient bars showing replicate means and SD without raw dots; f: vertically offset two-family
PDOS with outline/light fill; g: illustrative reaction barriers with a designated step in the second active primary; h: temperature-XRD map with aligned colourbar; i: two Nyquist model curves.
Scientific conventions and mock model parameters are exported beside the figure. No
surface-phase identification, spin assignment or experimental rate-control inference
is implied. Both colourbars reference ordinary 1.25:1 frames, never narrowed neighbours.

## Other maintained chemistry recipes

```bash
python scripts/preview_approved_palette.py OUTPUT_DIRECTORY
python scripts/preview_template.py OUTPUT_DIRECTORY
```

The first is the earlier abc layout with current colours: three-colour XPS (explicit
Primary 3 yellow), paired lines and four-layer no-error stacks. The second preserves the prior
3×3 geometry/uncertainty stress test: GC, paired curves, cumulative-error stacks, XPS,
twin axes, six-layer stacks, CV, XRD and Raman. The current palette is applied; prior
synthetic blue/red fixture keys are migrated to primary1/primary2 without altering values.
The six-colour fixture keeps a documented source-key mapping inside its script.

All tests exercise the fixed Arial typography, 4.5 pt paired markers, bar margins,
14 mm row and 16 mm column gaps and standard colourbar boundary. Numerical parameters and editable
SVG/PDF/PNG/TIFF accompany the source. Historical galleries are structural references,
not active colours/fonts or scientific processing instructions.
