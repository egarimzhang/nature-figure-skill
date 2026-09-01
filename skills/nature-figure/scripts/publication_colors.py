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


# Exact four-level primary anchors. Primary 3/4 are mutually exclusive warm
# alternatives in ordinary use; do not place them in the same figure.
PRIMARY = {
    'primary1': {'light':'#D9DBEF','mid':'#9FA5D6','main':'#666EB0','outline':'#4D5384'},
    'primary2': {'light':'#F9E3E0','mid':'#F0BAB0','main':'#E0725E','outline':'#B35B4B'},
    'primary3': {'light':'#FCE3C8','mid':'#F7CE9A','main':'#F7BC71','outline':'#E39C40'},
    'primary4': {'light':'#FFD2AA','mid':'#FFA450','main':'#DE6D04','outline':'#BF5E04'},
}
AUXILIARY_ANCHORS = {'cyan':'#A0DBCC','blue':'#9AC9DB','violet':'#D7BDDB'}
SCHEMES = {
    'primary1/primary2': ('primary1','primary2'),
    'primary1/primary3': ('primary1','primary3'),
    'primary1/primary4': ('primary1','primary4'),
}
SCHEME_ON_REQUEST = {
    # Primary 3 and 4 are alternatives and never enter one automatic sequence together.
    'primary1/primary2': ('primary3','cyan','blue','violet'),
    'primary1/primary3': ('primary2','cyan','blue','violet'),
    'primary1/primary4': ('cyan','blue','violet'),
}
DEFAULT_SCHEME = 'primary1/primary2'
CORE_ORDER = SCHEMES[DEFAULT_SCHEME]  # compatibility: active families of the default scheme
AUXILIARY_ORDER = SCHEME_ON_REQUEST[DEFAULT_SCHEME]  # compatibility: default on-request order
FAMILIES = {name:dict(values) for name,values in PRIMARY.items()}
for name,anchor in AUXILIARY_ANCHORS.items():
    # main/mid are helper aliases of the same anchor, not distinct prescribed swatches.
    FAMILIES[name] = {'anchor':anchor,'main':anchor,'mid':anchor,
                      'outline':blend(anchor,'#000000',.22)}
for name,family in FAMILIES.items():
    family['fill_tip']=family['main']
    family['fill_base']=blend(family['main'],amount=.38)
    family['bar_tip']=family.get('light',family['mid'])
    family['bar_base']=blend(family['bar_tip'],amount=.08)
    family['line']=family['outline']  # Deprecated compatibility role, never curve default.
    family['pair_light']=family['mid']  # Deprecated role; new primary pairs read mid.

NEUTRALS = {'black': '#000000', 'dark': '#4D4D4D', 'mid': '#767676',
            'light': '#CFCECE', 'pale': '#F2F2F2', 'white': '#FFFFFF'}
BAR_ALPHA = 1.0
FILL_ALPHA_BASE, FILL_ALPHA_TIP = 0.40, 0.82
CLOSED_FILL_ROLE = 'light'


def resolve_scheme(scheme=DEFAULT_SCHEME):
    """Return two active primary names from a registered name or exact pair."""
    if scheme is None:
        scheme = DEFAULT_SCHEME
    if isinstance(scheme, str):
        try:
            return SCHEMES[scheme]
        except KeyError as exc:
            raise ValueError(f'Unknown primary scheme: {scheme!r}') from exc
    pair=tuple(scheme)
    if pair not in SCHEMES.values():
        raise ValueError(f'Unregistered primary pair: {pair!r}')
    return pair


def scheme_name(scheme=DEFAULT_SCHEME):
    pair=resolve_scheme(scheme)
    return next(name for name,value in SCHEMES.items() if value==pair)


def closed_shape_style(family='primary1', alpha=0.65):
    """Default non-peak closed geometry: light face with outline boundary."""
    if family not in PRIMARY:
        raise ValueError('Closed-shape defaults require a four-level primary family.')
    return {'facecolor':FAMILIES[family][CLOSED_FILL_ROLE],
            'edgecolor':FAMILIES[family]['outline'],'alpha':alpha}


def category_colors(count, role='main', families=None, *, allow_auxiliary=False,
                    scheme=DEFAULT_SCHEME):
    """Default: active two-primary scheme. Opt-in extension follows its priority.

    Set allow_auxiliary only for an explicit auxiliary/multi-colour request, not
    because a dataset has more rows. Explicit families retain requested identities/order.
    """
    active=resolve_scheme(scheme)
    order=SCHEME_ON_REQUEST[scheme_name(scheme)]
    names=list(families) if families is not None else list(active)+(list(order) if allow_auxiliary else [])
    if 'primary3' in names and 'primary4' in names:
        raise ValueError('Primary 3 yellow and Primary 4 orange are mutually exclusive.')
    if count < 0 or count > len(names):
        raise ValueError('More categories than assigned colours: use markers/panels or request auxiliary colours.')
    return [FAMILIES[name][role] for name in names[:count]]


def stack_levels(family='primary1', *, count=3, reverse=False):
    """Literal solid swatches: three main/mid/light or four outline/main/mid/light.

    Reverse the second three-layer family for an explicit six-component stack.
    This never reorders data or supplies unrequested auxiliary families.
    """
    if family not in PRIMARY:
        raise ValueError('Auxiliaries have one anchor; explicitly design any extra stack levels.')
    if count not in (3, 4):
        raise ValueError('Use 3 or 4 levels, or explicitly design another stack mapping.')
    roles = ('main', 'mid', 'light') if count==3 else ('outline', 'main', 'mid', 'light')
    levels = [FAMILIES[family][role] for role in roles]
    return levels[::-1] if reverse else levels


def apply_color_style():
    """Colour-only style; leaves font sizes, dimensions and line widths alone."""
    mpl.rcParams.update({
        'axes.prop_cycle': mpl.cycler(color=category_colors(2, 'main', scheme=DEFAULT_SCHEME)),
        'axes.edgecolor': NEUTRALS['dark'], 'axes.labelcolor': NEUTRALS['dark'],
        'xtick.color': NEUTRALS['dark'], 'ytick.color': NEUTRALS['dark'], 'text.color': NEUTRALS['dark'],
        'grid.color': NEUTRALS['light'], 'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#FFFFFF',
    })
    # The Matplotlib cycle repeats after two; explicitly assign and validate
    # identities for every multi-series figure rather than relying on cycling.


def sequential_cmap(family='primary1'):
    f=FAMILIES[family]
    if family in PRIMARY:
        colors=[blend(f['main'],amount=.94),f['light'],f['mid'],f['main'],f['outline']]
    else:
        # A temporary numeric ramp, not a fixed categorical auxiliary ladder.
        colors=[blend(f['anchor'],amount=.94),f['anchor'],f['outline']]
    return mpl.colors.LinearSegmentedColormap.from_list(family+'_sequential',colors)


def diverging_cmap(scheme=DEFAULT_SCHEME):
    """Signed quantities only: zero neutral, ends use the active primary pair."""
    negative,positive=resolve_scheme(scheme)
    return mpl.colors.LinearSegmentedColormap.from_list('primary_signed',
        [FAMILIES[negative]['outline'],FAMILIES[negative]['main'],FAMILIES[negative]['light'],
         '#FAFAFA',FAMILIES[positive]['light'],FAMILIES[positive]['main'],FAMILIES[positive]['outline']])


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


def gradient_bar(ax, position, value, family='primary1', baseline=0, width=0.60,
                 horizontal=False, gradient=False, tip_color=None, base_color=None, alpha=BAR_ALPHA):
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
        patch.set_edgecolor(f['outline'])
        patch.set_linewidth(.75)
        patch.set_alpha(alpha)
        ax.add_patch(patch)
        return patch
    return _gradient(ax, patch, start, end, base, tip, alpha, alpha)


def raw_point_offsets(count, width, central_fraction=.40):
    """Deterministic positions spanning the central fraction of a bar's width."""
    if count < 1 or width <= 0 or not 0 < central_fraction <= 1:
        raise ValueError('Expected positive count/width and central_fraction in (0,1].')
    return np.linspace(-central_fraction/2,central_fraction/2,count)*width


def raw_data_bar(ax, position, values, family='primary1', width=.56,
                 error_kind=None, label=None, horizontal=False):
    """Mean bar with optional SD/SEM and every raw value; never invent uncertainty.

    The solid bar has a light face and outline boundary. Raw observations have light
    faces/main edges at their true value, evenly spanning the central 40% of bar width.
    Bar errors are neutral dark and topmost. Pass error_kind='sd' or 'sem' explicitly.
    """
    values=np.asarray(values,dtype=float)
    if values.ndim != 1 or len(values) < 1 or not np.isfinite(values).all():
        raise ValueError('Expected one or more finite raw observations.')
    if family not in PRIMARY:
        raise ValueError('Raw-data bars require a four-level primary family.')
    if horizontal:
        raise NotImplementedError('Adapt raw-point coordinates explicitly for horizontal bars.')
    if error_kind not in (None,'sd','sem'):
        raise ValueError("error_kind must be None, 'sd', or 'sem'.")
    if error_kind is not None and len(values) < 2:
        raise ValueError('At least two observations are required for SD/SEM.')
    f=FAMILIES[family];mean=float(values.mean());offsets=raw_point_offsets(len(values),width)
    bar=ax.bar(position,mean,width=width,facecolor=f['light'],edgecolor=f['outline'],
               linewidth=.75,label=label,zorder=1)
    points=ax.plot(position+offsets,values,ls='none',marker='o',ms=3.,mfc=f['light'],
                   mec=f['main'],mew=.45,zorder=4)
    error=None;container=None
    if error_kind is not None:
        error=float(values.std(ddof=1))
        if error_kind=='sem': error/=np.sqrt(len(values))
        container=ax.errorbar(position,mean,yerr=error,fmt='none',ecolor=NEUTRALS['dark'],
                              elinewidth=.75,capsize=1.8,capthick=.75,zorder=8)
    return {'bar':bar,'points':points,'errorbar':container,'mean':mean,
            'error':error,'offsets':offsets}


def gradient_peak(ax, x, y, family='primary1', baseline=0,
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
