# Physical composition patterns

See layout-contract.md for authoritative defaults; api.md for executable signatures.

## Regular rows

For a 180 mm three-column grid, use 60 mm pitches, left axes at 12/72/132 mm and
46 mm plotting widths, leaving 14 mm between column frames. Height is 46/1.3 mm;
row pitch starts at that height + 14 mm, then increases only as actual upper/lower
text requires, not arbitrary subplot hspace. Add panel labels before QA and preserve
common row top/bottom edges. Adjust margins rather than allowing text collisions.

## Twin axes

```python
right=make_twin_axis(ax)
ax.set_ylabel('Selectivity (%)')
right.set_ylabel('Conversion (%)')
# Set all data, limits, ticks and legends before measuring.
width_mm=fit_twin_to_width(ax,right,target_right_mm=178)
```

Left x/height stay fixed; decorated right edge fits the row's desired envelope.
Do not change data/scales merely to make curves align. Labels anchored to axes move
correctly. Extra right axes/colourbars count toward occupied width and may require
horizontal repositioning of neighbouring panels, not strict cross-row columns.

## Colourbar/image panels

Keep common row top/bottom frame edges. Align the colourbar right border to an ordinary
unshortened reference, not to a nearby twin's compromised frame or text envelope:

```python
# b is an ordinary panel; e has already been narrowed to fit right-axis text.
# h uses the same nominal column left edge. This helper requires aspect='auto'.
cax=add_aligned_colorbar_axis(h, reference_ax=b)
im=h.imshow(intensity, aspect='auto', origin='lower', cmap=sequential_cmap('blue'))
cb=h.figure.colorbar(im, cax=cax)
cax.tick_params(pad=STYLE['colourbar_tick_pad'])
```

Without an ordinary reference, pass `reference_right_mm` from the nominal grid.
For a 46 mm column allocation, 1.8 mm bar and 2 mm gap leave 42.2 mm for the heatmap.
Colourbar numbers lie outside the aligned edge; check actual text collisions and panel
letters, not only the union boxes. A compact title may sit above the bar. Do not squeeze
fonts or distort intrinsic/equal aspect to satisfy decorative alignment.

## Legends and overlays

No opaque boxes or frames by default. Keep legend order consistent; use empty spaces,
an external strip or several columns. 100% stacks often need a top/outside legend.
Leave panel-letter and title space. Inset boxes and arrows must not obscure evidence.
Single-family sequential levels should be labelled with the ordered condition, not
arbitrary colours. White annotation ink is reserved for dark fill contrast.

## Bar-edge padding

```python
# Flatten all actual centres/widths for grouped bars; list each stack only once.
set_bar_padding(ax, positions=centres, widths=bar_widths)
# For horizontal bars: axis='y'. Preserve an explicit requested range instead.
```

The helper derives limits from outer edges, preserving data and axis direction. Use
current actual widths, not a nominal group centre alone; include error extents or other
observations separately when they require a wider range.
