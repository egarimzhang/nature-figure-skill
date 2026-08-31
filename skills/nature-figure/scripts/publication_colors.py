"""Canonical colour definitions and editable gradient helpers.

Copy the relevant definitions/helpers into delivered plotting scripts; never make
the deliverable depend on this skill's installation path. Python/Matplotlib only.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib as mpl
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon, Rectangle


def blend(color, target='#FFFFFF', amount=0.2):
    """Mix RGB channels; this is a styling tint, not a perceptual data scale."""
    if not 0 <= amount <= 1:
        raise ValueError('amount must be between zero and one')
    a, b = np.array(mpl.colors.to_rgb(color)), np.array(mpl.colors.to_rgb(target))
    return mpl.colors.to_hex((1 - amount) * a + amount * b).upper()


# Exact approved anchors. Historical blue/red keys mean primary 1/2; primary 1
# is now blue-violet, distinct from the explicitly enabled auxiliary violet.
# Colour roles are styling choices, not scientific values or category importance.
FAMILIES = {
    'blue': {'light': '#DBDBDB', 'mid': '#C5C5E0', 'main': '#666EB0', 'outline': '#3F3770'},
    'red': {'light': '#DBD1B8', 'mid': '#E0A988', 'main': '#E0725E', 'outline': '#B35B4B'},
    'orange': {'main': '#F3962F', 'light': '#FACC8F'},  # explicit user request only
    'teal': {'main': '#42949E'},                       # explicit user request only
    'violet': {'main': '#9A4D8E'},                     # explicit user request only
}
for name, family in FAMILIES.items():
    main = family['main']
    family.setdefault('mid', blend(main, amount=0.22))
    family.setdefault('light', blend(main, amount=0.58))
    family.setdefault('outline', blend(main, '#000000', 0.22 if name=='orange' else 0.15))
    family['line'] = family['outline']  # Deprecated compatibility alias; never a curve default.
    family['pair_light'] = family['mid']  # Deprecated alias; new paired curves use main/mid.
    family['bar_tip'] = family['mid']
    family['bar_base'] = blend(family['mid'], amount=0.18)
    family['fill_tip'] = main
    family['fill_base'] = blend(main, amount=0.38)

NEUTRALS = {'black': '#000000', 'dark': '#4D4D4D', 'mid': '#767676',
            'light': '#CFCECE', 'pale': '#F2F2F2', 'white': '#FFFFFF'}
CORE_ORDER = ('blue', 'red')
AUXILIARY_ORDER = ('orange', 'teal', 'violet')
BAR_ALPHA = 1.0
FILL_ALPHA_BASE, FILL_ALPHA_TIP = 0.40, 0.82


def category_colors(count, role='main', families=None):
    """Explicit overflow instead of silently cycling colours or dropping data.

    Supply families only after deciding their semantics; orange/teal/violet require an
    explicit user request. A red+teal combination needs separate justification.
    """
    names = list(CORE_ORDER if families is None else families)
    if count < 0 or count > len(names):
        raise ValueError('More categories than assigned colours: choose markers, panels, or ask the user.')
    return [FAMILIES[name][role] for name in names[:count]]


def stack_levels(family='blue', *, count=3, reverse=False):
    """Literal solid swatches: three main/mid/light or four outline/main/mid/light.

    Reverse the second three-layer family for an explicit six-component stack.
    This never reorders data or supplies unrequested auxiliary families.
    """
    if count not in (3, 4):
        raise ValueError('Use 3 or 4 levels, or explicitly design another stack mapping.')
    roles = ('main', 'mid', 'light') if count==3 else ('outline', 'main', 'mid', 'light')
    levels = [FAMILIES[family][role] for role in roles]
    return levels[::-1] if reverse else levels


def apply_color_style():
    """Colour-only style; leaves font sizes, dimensions and line widths alone."""
    mpl.rcParams.update({
        'axes.prop_cycle': mpl.cycler(color=category_colors(len(CORE_ORDER), 'main')),
        'axes.edgecolor': NEUTRALS['dark'], 'axes.labelcolor': NEUTRALS['dark'],
        'xtick.color': NEUTRALS['dark'], 'ytick.color': NEUTRALS['dark'], 'text.color': NEUTRALS['dark'],
        'grid.color': NEUTRALS['light'], 'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#FFFFFF',
    })
    # The Matplotlib cycle repeats after two; explicitly assign and validate
    # identities for every multi-series figure rather than relying on cycling.


def sequential_cmap(family='blue'):
    f = FAMILIES[family]
    return mpl.colors.LinearSegmentedColormap.from_list(
        family + '_sequential', [blend(f['main'], amount=0.94), f['light'], f['mid'], f['main'], f['outline']])


def diverging_cmap():
    return mpl.colors.LinearSegmentedColormap.from_list(
        'blue_neutral_coral', [FAMILIES['blue']['outline'], NEUTRALS['pale'], FAMILIES['red']['outline']])


def _gradient(ax, patch, start, end, base_color, tip_color, base_alpha, tip_alpha, steps=96):
    """Linear-axis gradient, with vector strips for PDF/PNG and native SVG export."""
    if ax.get_xscale() != 'linear' or ax.get_yscale() != 'linear':
        raise ValueError('This gradient helper supports linear Cartesian axes only; adapt explicitly for other scales.')
    if not 0 <= base_alpha <= 1 or not 0 <= tip_alpha <= 1 or steps < 2:
        raise ValueError('Invalid opacity or gradient resolution')
    records = getattr(ax.figure, '_publication_gradients', [])
    gid = f'publication-gradient-{len(records)}'
    patch.set_gid(gid + '-shape')
    patch.set_facecolor('none')
    patch.set_edgecolor('none')
    ax.add_patch(patch)
    verts = patch.get_path().transformed(patch.get_patch_transform()).vertices
    xmin, ymin = verts.min(axis=0)
    xmax, ymax = verts.max(axis=0)
    vertical = start[0] == end[0]
    lo, hi = (start[1], end[1]) if vertical else (start[0], end[0])
    polys, colors = [], []
    c0, c1 = np.array(mpl.colors.to_rgb(base_color)), np.array(mpl.colors.to_rgb(tip_color))
    for i in range(steps):
        u, v = i / steps, (i + 1) / steps
        a, b = lo + (hi - lo) * u, lo + (hi - lo) * v
        if vertical:
            polys.append([(xmin, a), (xmax, a), (xmax, b), (xmin, b)])
        else:
            polys.append([(a, ymin), (b, ymin), (b, ymax), (a, ymax)])
        t = (u + v) / 2
        colors.append((*((1-t)*c0+t*c1), (1-t)*base_alpha+t*tip_alpha))
    collection = PolyCollection(polys, facecolors=colors, edgecolors='none',
                                antialiased=False, zorder=patch.get_zorder())
    collection.set_clip_path(patch)
    collection.set_clip_box(ax.bbox)
    collection.set_gid(gid + '-strips')
    ax.add_collection(collection)
    records.append(dict(gid=gid, ax=ax, start=start, end=end, base=base_color,
                        tip=tip_color, a0=base_alpha, a1=tip_alpha))
    ax.figure._publication_gradients = records
    return patch


def gradient_bar(ax, position, value, family='blue', baseline=0, width=0.60,
                 horizontal=False, gradient=True, tip_color=None, base_color=None, alpha=BAR_ALPHA):
    f = FAMILIES[family]
    tip, base = tip_color or f['bar_tip'], base_color or f['bar_base']
    endpoint = baseline + value
    if horizontal:
        patch = Rectangle((baseline, position-width/2), value, width, zorder=2)
        start, end = (baseline, position), (endpoint, position)
    else:
        patch = Rectangle((position-width/2, baseline), width, value, zorder=2)
        start, end = (position, baseline), (position, endpoint)
    if not gradient or value == 0:
        patch.set_facecolor(tip)
        patch.set_edgecolor('none')
        patch.set_alpha(alpha)
        ax.add_patch(patch)
        return patch
    return _gradient(ax, patch, start, end, base, tip, alpha, alpha)


def gradient_peak(ax, x, y, family='blue', baseline=0,
                  alpha_base=FILL_ALPHA_BASE, alpha_tip=FILL_ALPHA_TIP):
    """Positive peak over a constant baseline; outline must be drawn separately.

    The gradient runs along the intensity axis, not along a chemical coordinate.
    For sloping baselines or signed differences, adapt geometry explicitly.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or len(x) < 2 or not np.isfinite([x, y]).all():
        raise ValueError('Expected finite paired 1-D samples')
    if not (np.all(np.diff(x) > 0) or np.all(np.diff(x) < 0)) or np.any(y < baseline) or y.max() <= baseline:
        raise ValueError('Expected monotonic x and a peak above the constant baseline')
    f = FAMILIES[family]
    vertices = np.vstack(([x[0], baseline], np.column_stack((x, y)), [x[-1], baseline]))
    patch = Polygon(vertices, closed=True, zorder=1)
    return _gradient(ax, patch, (float(x.mean()), baseline), (float(x.mean()), float(y.max())),
                     f['fill_base'], f['fill_tip'], alpha_base, alpha_tip)


def save_editable_svg(fig, filename):
    """Save exact canvas size, replacing gradient strips with native SVG gradients.

    Finish layout and set limits first. Tight cropping is intentionally unsupported
    here because it shifts the SVG coordinate origin. Use explicit subplot margins.
    PDF/PNG/TIFF use normal fig.savefig and retain the same appearance (PDF strips
    are vector objects, but not single editable gradient stops).
    """
    with mpl.rc_context({'svg.fonttype': 'none', 'savefig.bbox': None}):
        fig.savefig(filename, format='svg', bbox_inches=None)
    records = getattr(fig, '_publication_gradients', [])
    if not records:
        return
    ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', ns)
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    tree = ET.parse(filename)
    root = tree.getroot()
    defs = root.find(f'{{{ns}}}defs')
    if defs is None:
        defs = ET.SubElement(root, f'{{{ns}}}defs')
    by_id = {el.get('id'): el for el in root.iter() if el.get('id')}
    parents = {child: parent for parent in root.iter() for child in parent}
    fig.canvas.draw()
    def svg_point(ax, point):
        px = ax.transData.transform(point)
        return px[0] * 72 / fig.dpi, (fig.bbox.height-px[1]) * 72 / fig.dpi
    for rec in records:
        gid = rec['gid']
        shape = by_id[gid + '-shape']
        path = shape.find(f'.//{{{ns}}}path')
        if path is None:
            raise RuntimeError('Missing exported gradient geometry')
        x0, y0 = svg_point(rec['ax'], rec['start'])
        x1, y1 = svg_point(rec['ax'], rec['end'])
        grad = ET.SubElement(defs, f'{{{ns}}}linearGradient', id=gid,
                             gradientUnits='userSpaceOnUse', x1=str(x0), y1=str(y0), x2=str(x1), y2=str(y1))
        for offset, color, alpha in [('0%', rec['base'], rec['a0']), ('100%', rec['tip'], rec['a1'])]:
            ET.SubElement(grad, f'{{{ns}}}stop', offset=offset,
                          attrib={'stop-color': color, 'stop-opacity': str(alpha)})
        path.set('style', f'fill: url(#{gid}); stroke: none')
        strips = by_id[gid + '-strips']
        parents[strips].remove(strips)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
