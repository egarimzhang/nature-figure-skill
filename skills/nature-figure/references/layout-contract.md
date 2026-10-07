# Final-size layout contract

These user-confirmed defaults replace earlier 75 mm plot / 11 pt text / 20 pt label /
1 pt axis examples. They are personal defaults, not universal publisher rules.

## Physical parameters

Numerical Python source: `../scripts/publication_style.py`, dictionary `STYLE`.
The default 1×3 reference canvas is 160 × 50.7 mm. Ordinary axes start at
10/65/120 mm, with 39 mm plot width and 31.2 mm height (1.25:1). Bottom
margin 12.5 mm, top margin 7 mm. The column frame-to-frame gap is 55 − 39 = 16 mm
and includes the next y-axis labels. Multirow canvases add appropriate row gaps; do
not fix every composite's height to this single-row example. Row frame-to-frame gaps
start at 14 mm, INCLUDING space for axis titles and legends. These are frame-edge
distances, not extra blank space after all text.
A 3×3 reference is 160 × 145.1 mm: bottom 10.5 mm, top 13 mm, three
31.2 mm frames and two 14 mm row gaps. Adjust margins/gaps for actual text without
shrinking fonts as the first response. Do not hard-code that total height for other figures.

| Element | Final-size default |
|---|---|
| Axis titles, numeric/category ticks | Arial 6 pt |
| Legends, peak labels, ordinary annotations | Arial 6 pt |
| Lowercase panel letters | Arial bold 10 pt |
| Axes and major/minor tick strokes | 0.75 pt, #000000 |
| Curves / point-line connections | 1.125 pt (1.5 × axis stroke) |
| Major / minor tick length | 2.5 / 1.5 pt, outward |
| Tick label pad / axis label pad | 1.5 / 2.5 pt |
| Point-line marker size / marker edge | 4.5 / 0.6 pt |
| Error line / cap stroke | 0.75 / 0.75 pt |
| Matplotlib error capsize / alpha | 1.8 pt / 1 |
| Panel-letter offset | left-axis x − 9.5 mm; baseline top-axis y + 1 mm |
| Row / column frame-to-frame gap | 14 / 16 mm, including labels and legends |

Always verify Arial regular/italic availability, including mathematical text. Never
silently fall back to another font. Superscripts/subscripts use normal typography
relative to the specified base size. Do not rasterize or outline text for convenience.

The 4.5 pt marker default includes corresponding legend markers. Dense spectral raw
points are a separate mark type (2.2 pt in the XPS test), not automatically enlarged.
Do not confuse Matplotlib `markersize` (pt) with scatter `s` (pt squared).

## Frames, ticks and labels

Ordinary data plots show all four frame sides. Left/bottom carry ticks; top/right are
plain unless they are an active additional axis. Set and label major x ticks by the
usual scale rules before deciding on x minors. If distinct observed x positions and
major x ticks correspond one-to-one, omit x minor ticks. If any observed x position
falls between major ticks, draw one short unnumbered midpoint minor tick per adjacent
major interval. For continuous linear x axes with extra major ticks not paired to data,
use the same midpoint rule. Do not create midpoint ticks on categorical axes;
log/symlog ticks need explicit scientifically appropriate placement. The y-axis retains
one unnumbered midpoint minor tick per adjacent major interval on continuous linear scales.
Aim for
roughly 4–6 readable major ticks, consistent precision, no unnecessary decimals or
opaque automatic numeric offsets. Do not force three-digit numbers on future plots:
that was only a spacing stress test. White background; no grid by default.

Axis titles use quantity followed by parenthesized units, with no quantity/unit slash.
Physical symbols italic; units/chemical formulas/descriptive words upright:
`$E$ (V vs. RHE)`, `Binding energy (eV)`, `Conversion (%)`. Ordinary text is pure black;
series-linked labels may use their colours.
Keep titles near tick labels using the stated pad, not a fixed far-left figure coordinate.
For a long axis title, preserve the 6 pt default first and keep it on one line when it fits. Try moving its position within
the decorated panel, using a clear multiplier above the axis to shorten
tick numbers, or wrapping only when needed. A vertical title may move downward no farther than the x-axis title's
height; avoid upward movement that can cover the panel letter. A horizontal title may
move left or right without crossing the y-axis title or right frame. Keep subplot frames
aligned. If these changes still cannot produce a balanced layout, reduce title size
modestly and inspect again at final dimensions.

## Limits and scientific scale

Bars normally retain a zero baseline. Bounded percentages such as conversion/selectivity
use 0–100%; inspect values AND error endpoints and report any overflow instead of
clipping. Percent changes may be signed or exceed 100 and are not automatically bounded.
Other limits follow data and comparison purpose; allow room for points, errors and labels.
Use common scales when comparisons require them. Changing limits for layout must not
hide observations, alter apparent comparisons or substitute for twin-axis width fitting.

Only apply a requested interval crop/axis break deliberately. A true omitted interval
needs separate scale segments, visible break marks and clear ticks; never imply one
continuous scale across a gap. A truncated bar needs an explicit truncation indication
and careful baseline treatment. Spectral axis direction and range follow supplied
requirements; do not infer XPS/Raman/XAS processing or assignments from style examples.

## Bar side margins

Measure from the OUTER edges of the first/last bar, including offsets and widths of
all bars in a group. Keep visible margins for ordinary and stacked bars. The approved
three-bar reference leaves about 4.11 mm on each side of a 39 mm frame. The helper starts
with 0.10546875 of the frame per side; adjust for bar count/group structure and required
axis coverage. Bar width remains about 50–60% of category spacing, not a way to hide
poor limits. Preserve observed positions and explicit user limits; never generalize the
example's 180–820 K range to new data. Linear category axes can use `set_bar_padding`;
nonlinear position axes need an explicit layout. See api.md.

## Alignment and mixed panels

Regular grids align left axes and share top/bottom frame edges within each row. Reserve
common margins using the widest tick/title bounds before locking axes positions.
Panel letters use the axes-left/top anchor plus fixed physical offsets, not the label
or tick-text extent. They follow any movement of their own panel.

Mixed layouts may break strict cross-row column alignment to accommodate multiple
right axes, colourbars, required image aspect ratios or useful right-edge alignment.
Keep each row's top/bottom frame alignment first, then balance the whole decorated
panel (frame + ticks + labels + legend/colourbar). Do not force every panel into an
identical rectangle. A right-edge reference is an available layout tool, not an
instruction to always align by the right axis.

Establish the column's standard right boundary from an ordinary, unshortened frame
or an explicit nominal grid boundary BEFORE accommodating extra axes. A narrowed twin
is a local accommodation, never a new reference for other panels. Do not cascade
width reductions down a column. User-specified alternative alignment takes precedence.

For one left/one right axis, preserve left edge and height while shortening the plot
width until its decorated right edge fits the intended envelope. Compute the reduction
from actual text; no fixed percentage. Draw each frame side once. Colourbars and extra
right axes consume real layout space; position neighbouring panels accordingly. The
1.25:1 default can yield to these requirements. Equal-aspect scientific geometry/images
must keep their meaningful aspect; do not stretch them to satisfy a decorative ratio.

For a heatmap plus right-side colourbar, align the colourbar's RIGHT BORDER to that
standard boundary, not to the shortened twin frame or the right edge of colourbar
text. Keep the heatmap left edge and row height; derive its width after subtracting
colourbar width (1.8 mm) and gap (2 mm). Tick-text pad starts at 3 pt, with text outside
the aligned border. In the maintained 3×3 preview, b frame and h colourbar right are
both 104 mm from the canvas left; e frame is about 96.32 mm after accommodating text.
These coordinates demonstrate the rule, not universal absolute positions.

Check adjacent panel letters, colourbar titles/ticks and axis titles at their actual
positions. Union bounding boxes can overlap in empty corners without real collisions;
inspect the individual artists as well. Remove needless trailing zeros (e.g. 0, 0.5, 1)
when appropriate, but do not reduce scientific precision for layout.

Legends are frameless and without opaque boxes; their ordering matches the data.
Use real empty space, outside placement or more columns instead of shrinking fonts.
Do not cover observations/errors/peaks. Reserve top space for panel letters and titles.

## Export

Draw directly at final physical size. Do not independently scale panel exports while
assembling a composite. Keep canvas bounds (no automatic tight crop that shifts origins).
SVG native gradients and editable text; PDF may contain vector gradient strips. Disclose
intentional raster maps while retaining editable axes, labels and source data. Keep all
colours/positions/alpha settings centralized in the delivered standalone script.
