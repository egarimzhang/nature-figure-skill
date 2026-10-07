# Unified colour contract

Canonical values live in `../scripts/publication_colors.py`; geometry lives in `layout-contract.md`. Choose one registered two-primary scheme per figure. Primary 3 yellow and Primary 4 orange are mutually exclusive alternatives and must not appear together. A scheme defines colour availability, not control/treatment semantics or a required area ratio.

## Four primary families

| Family / code key | light | mid | main | outline |
|---|---|---|---|---|
| Primary 1, blue-violet / primary1 | #D9DBEF | #9FA5D6 | #666EB0 | #4D5384 |
| Primary 2, coral / primary2 | #F9E3E0 | #F0BAB0 | #E0725E | #B35B4B |
| Primary 3, yellow / primary3 | #FCE3C8 | #F7CE9A | #F7BC71 | #E39C40 |
| Primary 4, orange / primary4 | #FFD2AA | #FFA450 | #DE6D04 | #BF5E04 |

Registered schemes are `primary1/primary2` (default), `primary1/primary3`, and `primary1/primary4`. The exact anchors are categorical starting points, not a perceptually uniform numeric scale.

## Scheme-specific on-request order

A third data colour requires an explicit multi-colour/on-request instruction; the number of data rows alone does not authorize more colours.

| Active scheme | First on-request colour | Further one-anchor auxiliaries |
|---|---|---|
| primary1/primary2 | primary3 yellow | cyan → blue → violet |
| primary1/primary3 | primary2 coral | cyan → blue → violet |
| primary1/primary4 | cyan | blue → violet |

Primary 3 and 4 never enter the same automatic sequence. Primary 4 may replace Primary 3 by explicit scheme choice, but it is not appended after Primary 3. For the Primary 1/4 scheme, cyan is deliberately the first extension; Primary 2 is not inserted automatically. Auxiliary anchors are cyan `#A0DBCC`, blue `#9AC9DB`, and violet `#D7BDDB`. Each has one anchor near mid/main strength, not a fixed four-level ladder; derive an outline only when needed. Explicit requested identity/order overrides the table. Never silently cycle, omit categories, or imply chemical identity/control status through palette position.

## Curves, points and errors

Independent curves use main. Two related measurements of one object use main + mid, reinforced with solid/filled versus dashed/open markers when helpful. Light is too weak for a routine equal-status measurement and is reserved for fills or deliberately backgrounded signals. `line` aliases outline and `pair_light` aliases mid for compatibility only.

Point-line markers remain 4.5 pt with 0.6 pt edges. Point-line error bars use their series family outline so overlapping uncertainties retain identity. Bar-chart error bars instead use the neutral axis colour `#000000` and sit above bars. Error stroke/cap thickness is 0.75 pt with capsize 1.8 pt. Error definition and n must be supplied or explicitly agreed; never invent uncertainty.

## Closed shapes and ordinary bars

A non-peak closed shape defaults to the primary family light face and outline boundary. This includes CV loops, PDOS areas, ordinary area polygons and comparable bounded regions; alpha 0.65 is the starting point when underlying marks must remain visible. Preserve acquisition order, baselines, signs and display-offset meaning. Do not use a fill merely because a path happens to be closed if area has no intended role.

Ordinary non-stacked bars use an opaque vertical gradient, main at the top and mid at the bottom, without an outline. For a negative bar, the end away from zero is main; horizontal bars follow the same away-from-baseline direction. When multiple observations are available, plot only their arithmetic mean and sample SD, without individual dots. Retain the raw observations in the reproducible data. Draw the neutral SD error bar last/topmost and state n. Do not invent an SD for a single or already summarized value. Use `summary_bar(..., error_kind='sd')` for replicates; an explicitly requested alternative uncertainty requires a stated definition.

Stacks remain literal solid levels because their internal colours encode components: three layers main/mid/light; four layers outline/main/mid/light; two requested three-layer families may use first main/mid/light and second light/mid/main. These mappings never reorder data. The number of layers, bars and replicates are independent.

## Peak-shaped gradient exception

Positive decomposed/fitted peaks such as XPS use a peak gradient rather than the ordinary closed-shape light fill. The family main (or an authorized auxiliary anchor) appears at the peak; a 38% white tint appears at the baseline; alpha increases from 0.40 to 0.82; an outline curve remains readable. This exception applies to scientifically meaningful peak-shaped spectral components, not arbitrary closed polygons. Raw points, total fit and background remain distinct and usually neutral. Preserve overlap visibility, export the component data and never infer peak assignments or fits merely for appearance.

## Maps, text and export

Axes, ticks, titles, bar errors and ordinary text use `#000000`. Series annotations may use the series colour; white text on a dark fill is a readability exception. Continuous intensity uses an ordered scale and interpretable colourbar. Signed changes use a meaningful neutral centre; `diverging_cmap(scheme=...)` uses the active pair. State reference and sign convention for difference maps. Keep source matrices for raster maps and document normalization, offsets and interpolation.

Deliver standalone editable Python, native SVG gradients, fixed-size SVG/PDF and preview PNG. Manual SVG edits do not update Python. See `tutorials.md` for maintained synthetic previews.
