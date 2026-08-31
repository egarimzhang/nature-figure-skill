# Unified colour contract

Canonical numbers: `../scripts/publication_colors.py`. Layout/typography remain in
[layout-contract.md](layout-contract.md). Historical gallery palettes are not defaults.

## Two primary families

Only primary 1 (blue-violet) and primary 2 (coral) are default category families, in
that order. Existing code/data keys `blue` and `red` retain compatibility; primary 1
is not the separate auxiliary `violet` family. Equal categories have equal standing:
never invent a control/hero or force a blue-area quota. Keep identities consistent
across linked panels. Do not replace these user-specified anchors by generated tints.

| Family / code key | light | mid | main | outline |
|---|---|---|---|---|
| Primary 1 / blue | #DBDBDB | #C5C5E0 | #666EB0 | #3F3770 |
| Primary 2 / red | #DBD1B8 | #E0A988 | #E0725E | #B35B4B |

Primary 1's neutral-grey light and primary 2's beige light are intentional. Within a
stack they identify components, not automatic references or missing data. Keep explicit
labels when a grey reference also occurs. The exact anchors are styling roles, not an
assertion that every adjacent swatch is a perceptually uniform numerical interval.

Orange, teal and auxiliary violet are all explicit-request-only supplements; never
silently add them for a third category. Existing auxiliary anchors remain orange main
#F3962F / mid #F6AD5D / light #FACC8F / outline #BE7525; teal main #42949E; violet main
#9A4D8E. Their remaining variants are defined in the canonical helper. Avoid red+teal
coexistence unless that combination is explicitly requested, e.g. the five-colour test.
More than two categories may need marker/line-style/facet distinctions or a colour
extension request. Do not cycle ambiguous colours, drop data, or infer authorization
from an old demonstration. A requested extension applies to the relevant figure/panel.

## Roles and paired measurements

| Role | Use |
|---|---|
| main | Independent curves/points and family anchor |
| mid | Ordinary bar fill; lighter of two related measurements |
| light | Light component/fill when appropriate; not a default thin curve |
| outline | Spectral boundaries or the deepest fourth stack level |

Curves normally use main. Two measurements of one object use main and mid, reinforced
with solid/filled versus dashed/hollow marks where appropriate. Primary-1 paired colours
are #666EB0/#C5C5E0; primary-2 colours are #E0725E/#E0A988. Do not use dark outline for
all ordinary curves or introduce an independent fifth colour tier. Thin marks may need
stronger colour than blocks; start from these roles and preserve family identity.

`line` is a deprecated alias of outline; `pair_light` is a deprecated alias of mid.
Keep aliases only for existing scripts. New code, docs and colour cards use the four
roles above; paired curves read `main`/`mid` directly.

Axes, ticks, titles and ordinary text use #4D4D4D. Grey baseline/control traces should
remain readable, not automatically faint or thin. Ordinary equal categories are not
automatically demoted to grey. Series-linked text may use series colour; white text
on dark fills is a readability exception.

## Bars and stacks

Ordinary bars use mid at the value endpoint, mid mixed with white by 18% at the baseline,
alpha 1. The positive/negative and vertical/horizontal rule is identical: deeper away
from baseline. Keep the same relative tint span, no outlines/shadows/3-D. Bar/group
width is about 50–60% of spacing, with outer-edge margins from layout-contract.md.

Stacks use solid, literal family swatches, not internal decorative gradients:

- Three components: `stack_levels(family)` gives main, mid, light bottom to top.
- Four components: `stack_levels(family, count=4)` gives outline, main, mid, light.
- Six components in two specified groups: first-family main/mid/light followed by
  second-family light/mid/main, using `reverse=True` for the second three-layer block.

These are optional mappings, never permission to reorder components or change data.
Number of bars and number of layers per bar are independent. Four layers means four
components in every bar. Per-layer values are opt-in, centred with contrasting ink.
Error bars are optional and require supplied or agreed uncertainty semantics; do not
invent replicates/errors or add errors to a requested no-error chart. When requested,
retain the cumulative-error rules in chart-types.md/API. The approved abc preview has
three bars, four layers each, 12 values, and no errors; it is not a universal bar count.

## Spectra, highlights and ordered curves

Positive fitted peaks use main at the tip and main mixed with 38% white at the baseline;
alpha goes from 0.40 at baseline to 0.82 at peak, with an outline-role boundary. These
are derived gradient endpoints, not substitutions for the literal light swatch. This
preserves visibility in crowded XPS. Adapt density/opacity without losing identity.
Overlaps do not imply extra components. Raw points, total fit and background use distinct
styles and readable greys. The helper supports constant baselines; adapt sloping/signed
cases explicitly. Never infer chemical assignments or processing from colour.

The approved GC comparison uses a grey before trace and primary-1 main after trace,
with documented offsets and no divider. A requested emerging-peak window uses second-
primary main at alpha 0.35, no border, behind both traces. Choose location from data;
this does not authorize orange highlights. CV/temperature series use ordered family
shades with explicit rate/cycle/temperature labels and readable grey references. Raman
may place primary 1 below primary 2 with a requested grey separator. Preserve observations;
do not smooth, normalize or fit merely for style.

## Numeric scales and editing

Continuous intensity needs an ordered, interpretable scale and colourbar. The sequential
helper progresses from a near-white main tint through light/mid/main/outline; inspect
lightness/contrast for the actual output. Signed deviations need a meaningful centre,
e.g. primary 1–pale neutral–primary 2. Categorical swatches do not mean signed numerical
values. Domain-specific elemental or microscopy-channel semantics take precedence.

Copy the needed helpers and colour constants into deliverable code; no installed-path
dependencies. Prefer native SVG gradients on a fixed canvas. PDF retains vector strips;
raster scientific heatmaps are allowed with disclosure/data. Manual SVG edits do not
update Python; propagate accepted edits into code for reproducibility. The approved
palette preview is documented in tutorials.md and executes the canonical helpers.
