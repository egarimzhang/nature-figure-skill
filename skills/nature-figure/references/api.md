# Maintained Python API

Use `publication_colors.py` and `publication_style.py` from `../scripts/`. Copy the
needed implementations into standalone deliveries. These files are the numeric source
of truth; do not paste styles from historical atlases.

## Style and layout

- `STYLE`: final-size dimensions, font sizes, strokes, ticks, marker and error settings.
- `apply_publication_style()`: verify Arial regular/italic; set pure-black complete-frame
  defaults, main curve colours and editable exports. Do not call old conflicting styles afterward.
- `style_axis(ax, categorical_x=False, categorical_y=False)`: four spines, correct ticks,
  y-axis midpoint linear minor ticks and pads. Call after creating the axis; specify categorical
  axes deliberately. X minors begin disabled until observed positions are known.
- `set_x_minor_ticks_from_data(ax, data_x)`: call after major x ticks and limits are final,
  passing distinct observed x positions rather than fit/grid samples. It omits x minors
  for one-to-one data/major-tick matches and otherwise enables one unnumbered midpoint
  per linear interval. Design log/symlog x minors explicitly. Labels use parenthesized
  units and italic physical symbols.
- `add_panel_label(ax, label, dx_mm=None, dy_mm=None)`: anchors to axes left/top with
  physical offsets. It follows later layout changes; no axis-title-bound anchoring.
- `make_twin_axis(ax)`: one visible copy of each frame edge; right ticks and black labels.
- `fit_twin_to_width(ax, right, target_right_mm=..., minimum_width_mm=20)`: solve decorated
  right boundary while retaining left edge and height. Set limits/text before fitting.
- `set_bar_padding(ax, positions, widths, axis='x', margin_fraction=None)`: centre-aligned
  bar edges determine linear position-axis limits. Scalar/vector widths; flatten grouped
  centres. Fraction is per side of final frame (default about 10.55%); keeps axis direction.
  Do not call over explicit user limits. For horizontal bars use `axis='y'`.
- `add_aligned_colorbar_axis(ax, reference_ax=None, reference_right_mm=None,
  width_mm=None, gap_mm=None, minimum_plot_width_mm=20)`: specify exactly one ordinary
  unshortened reference axis or nominal figure-mm right boundary. Preserve map left/height,
  solve width, return colourbar axis whose right border aligns to the standard boundary.
  Defaults: 1.8 mm width/2 mm gap; rejects fixed aspect. Labels need separate spacing QA.
- `set_percentage_axis(ax, values=..., axis='y', limits=(0,100))`: validates supplied
  values/error endpoints; raises rather than silently clipping overflows.

```python
import matplotlib.pyplot as plt
from publication_style import *
from publication_colors import *
apply_publication_style()
fig=plt.figure(figsize=(160/25.4,50.7/25.4))
ax=fig.add_axes([10/160,12.5/50.7,39/160,31.2/50.7])
style_axis(ax)
ax.set(xlabel=r'$T$ (K)',ylabel='Conversion (%)')
ax.set_xticks([300,500,700])
set_x_minor_ticks_from_data(ax,[300,500,700])
add_panel_label(ax,'a')
# Plot real observations and supplied/defined errors here; set limits to include them.
save_editable_svg(fig,'figure.svg')
fig.savefig('figure.pdf',bbox_inches=None)
```

## Colours and gradients

- `PRIMARY`, `FAMILIES`: four exact light/mid/main/outline primary families plus derived
  bar/fill helpers. Primary 3 yellow and Primary 4 orange are mutually exclusive.
  Migrate old source keys explicitly; do not silently reinterpret old data identities. `line` aliases outline; `pair_light` aliases
  mid for compatibility only. New curves use main, paired measurements main/mid.
- `SCHEMES`, `SCHEME_ON_REQUEST`, `resolve_scheme(scheme)`: registered primary 1/2,
  1/3 and 1/4 pairs and their non-cycling extension order.
- `category_colors(count, role='main', families=None, allow_auxiliary=False, scheme=...)`:
  defaults to the active pair and rejects overflow. Authorized extension follows the
  scheme-specific order; explicit family identity/order wins.
- `stack_levels(family='primary1', count=3, reverse=False)`: three literal main/mid/light
  swatches, or count=4 for outline/main/mid/light. Other counts raise; design an explicit
  mapping. Auxiliaries reject fixed stack ladders; derive them only when requested. Reverse the second three-layer block for requested six-component two-family stacks.
- `blend(color, target='#FFFFFF', amount=...)`: RGB styling tint, not a data scale.
- `closed_shape_style(family='primary1',alpha=.65)`: light face/outline boundary for
  non-peak closed areas.
- `gradient_bar(..., gradient=True, ...)`: ordinary default is an opaque mid-at-baseline,
  main-at-outer-end gradient without an outline. For positive bars this is top-main/bottom-mid.
- `summary_bar(ax,position,values,family,width,error_kind='sd',label=None)`: mean bar
  with sample SD by default, no individual dots, and a neutral top error bar. Retain
  raw observations in source data. For a single supplied summary, use `error_kind=None`
  or `gradient_bar` directly. The return value includes an optional solid-colour legend
  proxy. `raw_data_bar` remains a compatibility alias but also omits raw dots.
- `raw_point_offsets(...)`: explicit opt-in helper for a user-requested raw-point overlay;
  it is not used by default bars.
- `gradient_peak(ax,x,y,family='primary1',baseline=0,alpha_base=.40,alpha_tip=.82)`:
  monotonic x, finite positive curve above constant baseline. Draw an outline separately.
- `sequential_cmap(family='primary1')`, `diverging_cmap(scheme=...)`: numeric scales.
- `save_editable_svg(fig, filename)`: after final layout, replace clipped gradient strips
  by editable native SVG gradients. Fixed canvas required; ordinary savefig handles PDF/raster.

## Stacked uncertainty

`stacked_bars(ax,x,replicates,colors,error_kind=...,error_scope='cumulative',
width=.6,labels=None,annotate=False)` takes shape `(n_replicates,n_bars,n_components)`.
Matched replicate stacks are summed along components BEFORE SD/SEM is computed.
It returns `(segment_means, cumulative_boundary_means, cumulative_errors)`.
Specify `error_kind='sd'` or `'sem'` explicitly and state n/meaning in the caption.
`error_scope='total'` shows only the total. `annotate=True` places each mean inside its
segment at 6 pt, with contrasting ink. Do not label cumulative uncertainty as segment
uncertainty or sum standard deviations. Provided asymmetric errors/CIs require their
own scientifically justified calculation. No invented errors for real data. When errors
are not requested or not supplied, draw solid `ax.bar` stacks directly without this
replicate/error helper; four layers do not imply four bars or automatic error bars.
