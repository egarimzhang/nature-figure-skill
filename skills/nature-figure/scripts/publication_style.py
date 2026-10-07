"""Final-size chemistry figure defaults; read layout-contract.md for semantics.

Copy this module and publication_colors into standalone delivered scripts.
No installed-skill path dependency is permitted in a delivered figure script.
"""
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager, transforms
from matplotlib.ticker import AutoMinorLocator, FixedLocator, NullLocator
from publication_colors import NEUTRALS, apply_color_style

STYLE = {
    'font': 'Arial', 'axis_font': 8.0, 'text_font': 7.5, 'panel_font': 12.0,
    'axis_width': 0.75, 'curve_width': 1.125,
    'major_length': 2.5, 'minor_length': 1.5,
    'tick_pad': 1.5, 'label_pad': 2.5,
    'error_width': 0.75, 'error_capsize': 1.8,
    'marker_size': 4.5, 'marker_edge': 0.6,
    'figure_width_mm': 180.0, 'plot_width_mm': 46.0, 'aspect': 1.3,
    'row_frame_gap_mm': 14.0, 'column_frame_gap_mm': 14.0,
    'multirow_bottom_mm': 10.5, 'multirow_top_mm': 13.0,
    'bar_edge_fraction': 0.10546875,  # accepted three-bar reference; editable per layout
    'colourbar_width_mm': 1.8, 'colourbar_gap_mm': 2.0, 'colourbar_tick_pad': 3.0,
    'cell_pitch_mm': 60.0, 'panel_dx_mm': -9.5, 'panel_dy_mm': 0.4,
}


def apply_publication_style():
    """Verify Arial regular/italic before drawing; never silently substitute."""
    for slant in ('normal', 'italic'):
        font_manager.findfont(font_manager.FontProperties(family=STYLE['font'],style=slant),
                              fallback_to_default=False)
    apply_color_style()
    mpl.rcParams.update({
        'font.family': STYLE['font'], 'font.size': STYLE['text_font'],
        'axes.labelsize': STYLE['axis_font'], 'axes.titlesize': STYLE['text_font'],
        'xtick.labelsize': STYLE['axis_font'], 'ytick.labelsize': STYLE['axis_font'],
        'legend.fontsize': STYLE['text_font'], 'legend.frameon': False,
        'axes.linewidth': STYLE['axis_width'], 'lines.linewidth': STYLE['curve_width'],
        'lines.markersize': STYLE['marker_size'], 'lines.markeredgewidth': STYLE['marker_edge'],
        'axes.spines.top': True, 'axes.spines.right': True, 'axes.grid': False,
        'mathtext.fontset': 'custom', 'mathtext.rm': 'Arial', 'mathtext.it': 'Arial:italic',
        'mathtext.bf': 'Arial:bold', 'mathtext.sf': 'Arial', 'mathtext.fallback': None,
        'svg.fonttype': 'none', 'pdf.fonttype': 42, 'savefig.bbox': None,
    })


def style_axis(ax, *, categorical_x=False, categorical_y=False):
    """Full frame; set x minors after plotting with set_x_minor_ticks_from_data."""
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color(NEUTRALS['dark'])
        spine.set_linewidth(STYLE['axis_width'])
    ax.tick_params(axis='both', which='major', direction='out', top=False, right=False,
                   width=STYLE['axis_width'], length=STYLE['major_length'],
                   pad=STYLE['tick_pad'], colors=NEUTRALS['dark'],labelsize=STYLE['axis_font'])
    ax.tick_params(axis='both', which='minor', direction='out', top=False, right=False,
                   width=STYLE['axis_width'],length=STYLE['minor_length'],
                   colors=NEUTRALS['dark'],labelbottom=False,labelleft=False,labelright=False,labeltop=False)
    ax.xaxis.set_minor_locator(NullLocator())
    ax._publication_categorical_x=bool(categorical_x)
    if categorical_y:
        ax.yaxis.set_minor_locator(NullLocator())
    elif ax.get_yscale() == 'linear':
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    # Log/symlog minor spacing requires a deliberate domain-specific choice.
    ax.xaxis.labelpad=STYLE['label_pad']
    ax.yaxis.labelpad=STYLE['label_pad']
    ax.set_facecolor('white')


def set_x_minor_ticks_from_data(ax, data_x):
    """Apply the observed-x rule after major ticks and data positions are finalized.

    Pass unique experimental/category centres, not fit-curve samples or grid lines.
    Categorical axes keep no minors; log/symlog axes need explicit tick design.
    Returns whether midpoint minors were enabled.
    """
    if ax.get_xscale() != 'linear':
        raise ValueError('Design minor ticks explicitly for a non-linear x axis.')
    if getattr(ax,'_publication_categorical_x',False):
        ax.xaxis.set_minor_locator(NullLocator())
        return False
    data=np.asarray(data_x,dtype=float).ravel()
    if data.size == 0 or not np.isfinite(data).all():
        raise ValueError('Expected finite observed x positions.')
    major=np.asarray(ax.get_xticks(),dtype=float)
    lo,hi=sorted(ax.get_xlim())
    major=np.sort(np.unique(major[(major>=lo)&(major<=hi)]))
    observed=np.sort(np.unique(data[(data>=lo)&(data<=hi)]))
    one_to_one=(len(observed)==len(major) and
                np.allclose(observed,major,rtol=1e-9,atol=1e-12))
    midpoints=(major[:-1]+major[1:])/2
    ax.xaxis.set_minor_locator(NullLocator() if one_to_one else FixedLocator(midpoints))
    return not one_to_one


def add_panel_label(ax, label, *, dx_mm=None, dy_mm=None):
    """Axes-left/top anchor + physical translation; follows later axes movement."""
    dx=STYLE['panel_dx_mm'] if dx_mm is None else dx_mm
    dy=STYLE['panel_dy_mm'] if dy_mm is None else dy_mm
    transform=ax.transAxes+transforms.ScaledTranslation(dx/25.4,dy/25.4,ax.figure.dpi_scale_trans)
    return ax.text(0,1,label,transform=transform,ha='left',va='baseline',
                   fontsize=STYLE['panel_font'],fontweight='normal',
                   color=NEUTRALS['dark'],clip_on=False)


def make_twin_axis(ax):
    """Draw each frame side only once; both y axes stay dark grey."""
    right=ax.twinx()
    style_axis(right)
    ax.spines['right'].set_visible(False)
    for side in ('left','bottom','top'):
        right.spines[side].set_visible(False)
    right.patch.set_visible(False)
    right.tick_params(axis='y',which='both',left=False,right=True,labelleft=False)
    right.tick_params(axis='y',which='major',labelright=True)
    right.tick_params(axis='y',which='minor',labelright=False)
    return right


def fit_twin_to_width(ax, right, *, target_right_mm, minimum_width_mm=20):
    """Preserve left edge/height; fit decorated right edge to a figure-mm target."""
    fig=ax.figure
    target=target_right_mm/25.4*fig.dpi
    for _ in range(5):
        fig.canvas.draw()
        renderer=fig.canvas.get_renderer()
        edge=max(a.get_tightbbox(renderer).x1 for a in (ax,right))
        p=ax.get_position()
        width=p.width+(target-edge)/fig.bbox.width
        if width*fig.get_figwidth()*25.4 < minimum_width_mm:
            raise ValueError('Right-axis decorations leave too little plot area; revise layout.')
        for a in (ax,right):
            a.set_position([p.x0,p.y0,width,p.height])
    fig.canvas.draw()
    return ax.get_position().width*fig.get_figwidth()*25.4


def set_bar_padding(ax, positions, widths, *, axis='x', margin_fraction=None):
    """Set linear category-axis limits from ALL outer bar edges (centre alignment).

    Supply individual centres/widths for grouped bars, or once per stack. Preserve
    positions and axis direction. Do not call when explicit limits should prevail.
    The margin is the fraction of final frame width/height on EACH side. The accepted
    46 mm, three-bar example leaves 4.85 mm. Nonlinear axes need explicit layout.
    """
    if axis not in ('x','y'):
        raise ValueError('axis must be x or y')
    if (ax.get_xscale() if axis=='x' else ax.get_yscale()) != 'linear':
        raise ValueError('Bar padding helper supports linear position axes only.')
    pos=np.atleast_1d(np.asarray(positions,dtype=float))
    width=np.broadcast_to(np.asarray(widths,dtype=float),pos.shape)
    fraction=STYLE['bar_edge_fraction'] if margin_fraction is None else margin_fraction
    if (pos.ndim!=1 or not pos.size or not np.isfinite(pos).all()
            or not np.isfinite(width).all() or np.any(width<=0)
            or not np.isfinite(fraction) or not 0<=fraction<.5):
        raise ValueError('Expected finite centres, positive widths and 0 <= margin < 0.5.')
    low=float(np.min(pos-width/2));high=float(np.max(pos+width/2))
    pad=(high-low)*fraction/(1-2*fraction)
    limits=(low-pad,high+pad)
    inverted=ax.xaxis_inverted() if axis=='x' else ax.yaxis_inverted()
    (ax.set_xlim if axis=='x' else ax.set_ylim)(limits[::-1] if inverted else limits)
    return limits


def add_aligned_colorbar_axis(ax, *, reference_ax=None, reference_right_mm=None,
                             width_mm=None, gap_mm=None, minimum_plot_width_mm=20):
    """Align colourbar RIGHT BORDER to an ordinary unshortened column reference.

    Specify one standard reference axis OR a pre-established figure-mm boundary;
    never pass an already narrowed twin as the reference. Keep plot left/height;
    colourbar labels lie outside this border and need separate collision checks.
    Call for aspect='auto' maps; scientifically fixed aspect needs explicit layout.
    """
    if (reference_ax is None)==(reference_right_mm is None):
        raise ValueError('Specify exactly one ordinary reference axis or standard right boundary.')
    fig=ax.figure;fw=fig.get_figwidth()*25.4
    if reference_ax is not None:
        if reference_ax.figure is not fig or reference_ax is ax:
            raise ValueError('Reference must be a separate ordinary axis in the same figure.')
        reference_right_mm=reference_ax.get_position().x1*fw
    width=STYLE['colourbar_width_mm'] if width_mm is None else width_mm
    gap=STYLE['colourbar_gap_mm'] if gap_mm is None else gap_mm
    p=ax.get_position();left=p.x0*fw
    plot_width=reference_right_mm-left-width-gap
    if (not np.isfinite([reference_right_mm,width,gap,minimum_plot_width_mm]).all()
            or width<=0 or gap<0 or minimum_plot_width_mm<=0
            or plot_width<minimum_plot_width_mm or reference_right_mm>fw):
        raise ValueError('Insufficient or invalid column space for plot and colourbar.')
    if ax.get_aspect()!='auto':
        raise ValueError('Fixed scientific aspect requires an explicit layout; do not stretch it.')
    ax.set_position([p.x0,p.y0,plot_width/fw,p.height])
    return fig.add_axes([(reference_right_mm-width)/fw,p.y0,width/fw,p.height])

def set_percentage_axis(ax, *, values, axis='y', limits=(0,100)):
    """Check data/error endpoints before applying bounded-percentage defaults.

    Supply error endpoints in values too. An explicit expanded range can be passed.
    This helper does not assume every quantity containing '%' is bounded.
    """
    values=np.asarray(values,dtype=float)
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError('Expected finite percentage values, including error endpoints.')
    lo,hi=limits
    if lo >= hi or values.min()<lo or values.max()>hi:
        raise ValueError('Values/error endpoints exceed percentage limits; review instead of clipping.')
    if axis not in ('x','y'):
        raise ValueError('axis must be x or y')
    (ax.set_ylim if axis=='y' else ax.set_xlim)(limits)


def stacked_bars(ax, x, replicates, colors, *, error_kind, error_scope='cumulative',
                 width=0.6, labels=None, annotate=False):
    """Stack means from matched replicates; SD/SEM computed BEFORE averaging.

    replicates shape = (replicates, bars, components). Error bars describe either
    cumulative boundary heights or total height, not isolated segment values.
    Specify error_kind explicitly ('sd' or 'sem'); never infer scientific meaning.
    CI or provided asymmetric errors need their own explicit statistical calculation.
    """
    v=np.asarray(replicates,dtype=float)
    x=np.asarray(x,dtype=float)
    if v.ndim!=3 or v.shape[0]<2 or v.shape[1]!=len(x) or not np.isfinite(v).all() or np.any(v<0):
        raise ValueError('Expected >=2 matched finite nonnegative replicate stacks.')
    if len(colors)!=v.shape[2] or (labels is not None and len(labels)!=v.shape[2]):
        raise ValueError('Assign one colour and label per component; do not drop segments.')
    if error_kind not in ('sd','sem') or error_scope not in ('cumulative','total'):
        raise ValueError('Explicit error kind and cumulative/total scope required.')
    mean=v.mean(axis=0)
    cumulative=v.cumsum(axis=2)
    boundary_mean=cumulative.mean(axis=0)
    error=cumulative.std(axis=0,ddof=1)
    if error_kind=='sem': error=error/np.sqrt(v.shape[0])
    base=np.zeros(len(x))
    for j,color in enumerate(colors):
        ax.bar(x,mean[:,j],bottom=base,width=width,color=color,edgecolor='none',
               label=labels[j] if labels else None,zorder=2)
        if annotate:
            rgb=np.asarray(mpl.colors.to_rgb(color))
            linear=np.where(rgb<=0.04045,rgb/12.92,((rgb+0.055)/1.055)**2.4)
            luminance=float(linear @ np.array([.2126,.7152,.0722]))
            ink='white' if luminance<0.25 else NEUTRALS['dark']
            for xx,yy,bb in zip(x,mean[:,j],base):
                ax.text(xx,bb+yy/2,f'{yy:g}',ha='center',va='center',
                        fontsize=STYLE['text_font'],color=ink,zorder=5)
        base+=mean[:,j]
    indices=range(v.shape[2]) if error_scope=='cumulative' else [v.shape[2]-1]
    for j in indices:
        ax.errorbar(x,boundary_mean[:,j],yerr=error[:,j],fmt='none',
                    ecolor=NEUTRALS['dark'],elinewidth=STYLE['error_width'],
                    capsize=STYLE['error_capsize'],capthick=STYLE['error_width'],zorder=4)
    return mean,boundary_mean,error
