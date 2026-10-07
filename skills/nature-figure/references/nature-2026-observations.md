# 2026 Nature Sample Observations

> Active styling comes from [layout-contract.md](layout-contract.md) and
> [color-contract.md](color-contract.md). Historical sizes, fonts and colour choices
> below are observations/examples, not overrides. Preserve explicitly requested panels.

This note captures page-level figure patterns observed from a local 2026 sample of `Nature`
papers, plus one `Nature Biomedical Engineering` paper used as a clinical / ML-adjacent
cross-check.

Sampled figure sources:

- `s41586-026-10408-8` — wide schematic-led materials figure with supporting quant panels
- `s41586-026-10426-6` — dark whole-brain image plate with repeated views
- `s41586-026-10393-y` — clinical triptych: longitudinal lines, forest plots, summary bars
- `s41586-026-10257-5` — dense categorical stacked-area panels with direct labels
- `s41586-026-10439-1` — asymmetric genomics figure with one dominant circular panel
- `Expert-level detection of pathologies...` — compact medical / ML figure conventions

## Archetype 1: Schematic-led composite

Seen in the printable meta-assemblies paper.

Actionable rules:

- Let the schematic occupy roughly `45–60%` of figure height.
- Keep sample identities consistent between schematic and supporting plots under the unified colour contract.
- Zoom callouts should use one repeated accent style across the figure, for example a single dashed red outline family.
- Reserve at least one supporting panel for a real-world photograph or experimental snapshot when the story needs scale validation.
- Supporting quantitative panels should be smaller, cleaner and less saturated than the schematic so the eye reads the page in the intended order.

## Archetype 2: Dark image plate

Seen in the astrocyte brain-network figure.

Actionable rules:

- Use a black facecolor only for the image plate region, not for the whole page.
- Pair grayscale context with one or two fluorescent channels; the sample repeatedly used cyan and magenta.
- Keep crops, scale bars and view boxes geometrically consistent across rows and columns.
- Use white gutters and white scale bars so the plate stays legible after print/export compression.
- Put row labels and channel labels directly on the image plate; avoid detached legends.

Preserve explicitly supplied image-channel meanings; there is no default channel palette.

## Archetype 3: Clinical triptych

Seen in the OTOF gene-therapy paper.

Actionable rules:

- Top row: line plots or longitudinal summaries, usually sharing one legend strip above the row.
- Middle row: forest-plot style effects with a dashed vertical reference line and light category bands.
- Bottom row: compact summary bars, often binary or stacked-percentage bars.
- Keep columns semantically parallel. If the first column is `ABR`, the next columns should reuse the same row logic rather than introducing a new layout.
- Baseline / reference series use readable grey; follow-up or intervention groups can use a restrained warm/cool sequence.

Recommended design signal:

- Legends belong outside the data region when there are many timepoints.
- Group bands in forest plots should be pale and subordinate, never more salient than the confidence intervals.

## Archetype 4: Dense categorical physical-science panel

Seen in the condensation-sequence figure.

Actionable rules:

- Direct-label regions when the plot has many semantically intrinsic categories.
- Use hatching or texture overlays when neighboring fills are close in luminance or may print poorly.
- Reuse the exact same axis limits and panel geometry across the full grid.
- Prefer embedded labels over a detached mega-legend when each panel repeats the same categorical structure.

## Archetype 5: Asymmetric mixed-modality figure

Seen in the rediploidization genomics figure.

Actionable rules:

- Do not force equal panel sizes. Let the biologically central panel dominate.
- Use small supporting plots around the hero panel to answer narrower questions.
- Keep a tight, reused color mapping across all modalities, for example `wave 1 / wave 2 / wave 3` or `baseline / highlight / neutral`.
- Use whitespace and alignment, not decorative frames, to signal grouping.

## Cross-cutting Nature rules from the sample

- Historical sampled panels used small bold letters; current user defaults instead use the 10 pt bold axes-anchored labels with baseline 1 mm above the frame in layout-contract.md.
- Figure pages are narrative, not dashboard-like. A dominant panel is normal.
- Legends are often omitted if direct labeling is possible.
- Background discipline matters more than ornament. White for charts, black only for image plates.
- Saturated colors are used sparingly and usually mean either a true experimental channel or a highlighted subgroup.
- When several modalities coexist, keep axis-heavy plots visually quieter than schematics or imaging panels.
- Gutters are slightly larger when dark panels touch light panels or when modalities change.

## Colour guidance

Historical examples illustrate layout, not active palette defaults. Use the unified
[colour contract](color-contract.md) for all new plots. Explicit image-channel
meanings are a domain exception, not a source of general category colours.

## What not to copy blindly

- Do not import a bright multi-hue palette just because one sampled physical-science figure used many fills. That only works when the categories are intrinsic phases/materials and directly labeled.
- Do not place all Nature figures on black backgrounds; that was specific to the imaging plate archetype.
- Do not force a legend into every panel. Many sampled figures read better with direct labels or one shared legend strip.
