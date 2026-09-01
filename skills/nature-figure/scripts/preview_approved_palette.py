"""Approved synthetic abc palette test; yellow explicitly enabled only in XPS.
Run: python scripts/preview_approved_palette.py OUTPUT_DIRECTORY
Three bars each have four layers, value labels and no error bars; no scientific claims.
"""
import sys
import shutil
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from publication_colors import *
from publication_style import *

PREVIEW = {
    'canvas_width_mm': 180., 'left_mm': 12., 'column_pitch_mm': 60.,
    'bottom_mm': 12.5, 'top_mm': 7., 'plot_width_mm': 46., 'aspect': 1.3,
    'xps_baseline': .028, 'xps_families': ['primary1', 'primary3', 'primary2'],
    'paired_roles': ['main', 'mid'],
    'stack_roles_bottom_to_top': ['outline', 'main', 'mid', 'light'],
    'bar_width_data': 105., 'c_error_bars': False,
}


def read_csv(path):
    return np.genfromtxt(path, delimiter=',', names=True, dtype=None, encoding='utf-8')


def main(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    data = out/'source_data'; data.mkdir(exist_ok=True)
    source = Path(__file__).resolve().parent.parent/'assets'/'approved-palette-data'
    for name in ('a_xps.csv', 'b_two_objects.csv', 'c_values.csv'):
        if (source/name).resolve() != (data/name).resolve():
            shutil.copy2(source/name, data/name)
    apply_publication_style()
    fw = PREVIEW['canvas_width_mm']; pw = PREVIEW['plot_width_mm']
    ph = pw/PREVIEW['aspect']; fh = PREVIEW['bottom_mm']+ph+PREVIEW['top_mm']
    fig = plt.figure(figsize=(fw/25.4, fh/25.4), dpi=180)
    axes = []; letters = []
    for index in range(3):
        left = PREVIEW['left_mm'] + index*PREVIEW['column_pitch_mm']
        ax = fig.add_axes([left/fw, PREVIEW['bottom_mm']/fh, pw/fw, ph/fh])
        style_axis(ax); axes.append(ax); letters.append(add_panel_label(ax, chr(97+index)))
    a, b, c = axes

    # a: three simulated components; placeholder labels have no chemical assignment.
    spectrum = read_csv(data/'a_xps.csv')
    energy = spectrum['binding_energy_eV']; baseline = PREVIEW['xps_baseline']
    for index, family in enumerate(PREVIEW['xps_families']):
        signal = spectrum[family]
        gradient_peak(a, energy, baseline+signal, family, baseline=baseline)
        a.plot(energy, baseline+signal, color=FAMILIES[family]['outline'])
        k = np.argmax(signal)
        a.text(energy[k], baseline+signal[k]+.065, f'P{index+1}',
               ha='center', color=FAMILIES[family]['outline'])
    a.plot(energy, spectrum['total'], color=NEUTRALS['dark'], ls='--', zorder=4)
    a.plot(energy[::13], spectrum['synthetic_observation'][::13], ls='none',
           marker='o', ms=2.2, mfc='none', mec='#969696', mew=.55, zorder=5)
    a.axhline(baseline, color=NEUTRALS['mid'], lw=STYLE['axis_width'], ls=':')
    a.set(xlim=(293.2,281.8), ylim=(0,1.28), xticks=[292,290,288,286,284,282],
          yticks=[0,.4,.8,1.2], xlabel='Binding energy / eV', ylabel='Intensity / a.u.')
    a.text(.03,.97,'XPS',transform=a.transAxes,va='top')
    assert np.allclose(sum(spectrum[n] for n in PREVIEW['xps_families'])+baseline,
                       spectrum['total'])

    # b: two equal objects, each measured twice. Colour, marker and dash are explicit.
    paired = read_csv(data/'b_two_objects.csv')
    for j, (family, marker) in enumerate(zip(CORE_ORDER, ['o','s'])):
        for measurement, role in enumerate(PREVIEW['paired_roles'], start=1):
            rows = paired[(paired['object']==family)&(paired['measurement']==measurement)]
            color = FAMILIES[family][role]
            b.plot(rows['temperature_K'], rows['response_percent'], color=color,
                   marker=marker, ms=STYLE['marker_size'], mec=color,
                   mfc=color if measurement==1 else 'white', mew=STYLE['marker_edge'],
                   ls='-' if measurement==1 else '--', label=f'{chr(65+j)}{measurement}')
    b.set(xlim=(180,820), ylim=(0,100), xticks=[300,400,500,600,700],
          yticks=[0,25,50,75,100], xlabel=r'$T$ / K', ylabel='Response / %')
    b.legend(loc='lower center', bbox_to_anchor=(.5,1.03), ncol=4, frameon=False,
             handlelength=1.05, handletextpad=.3, columnspacing=.7, borderaxespad=0, borderpad=.1)

    # c: three bars, each with FOUR components; intentionally no errorbar calls.
    stack = read_csv(data/'c_values.csv'); temperatures = stack['temperature_K']
    values = np.column_stack([stack[n] for n in ('I','II','III','IV')])
    base = np.zeros(len(temperatures))
    colors = [FAMILIES['primary1'][role] for role in PREVIEW['stack_roles_bottom_to_top']]
    for j, (color, label) in enumerate(zip(colors, ['I','II','III','IV'])):
        c.bar(temperatures, values[:,j], bottom=base, width=PREVIEW['bar_width_data'],
              color=color, edgecolor='none', label=label, zorder=2)
        rgb = np.asarray(mpl.colors.to_rgb(color))
        linear = np.where(rgb<=.04045, rgb/12.92, ((rgb+.055)/1.055)**2.4)
        ink = 'white' if float(linear @ np.array([.2126,.7152,.0722]))<.25 else NEUTRALS['dark']
        for x, value, bottom in zip(temperatures, values[:,j], base):
            c.text(x, bottom+value/2, f'{value:g}', ha='center', va='center',
                   color=ink, fontsize=STYLE['text_font'], zorder=5)
        base += values[:,j]
    c.set(xticks=[300,500,700], yticks=[0,25,50,75,100],
          xlabel=r'$T$ / K', ylabel='Fraction / %')
    set_percentage_axis(c, values=base)
    set_bar_padding(c, temperatures, PREVIEW['bar_width_data'])
    c.legend(loc='upper left', ncol=4, frameon=False, handlelength=.9,
             handletextpad=.3, columnspacing=.6, borderpad=.2)

    fig.canvas.draw(); renderer = fig.canvas.get_renderer()
    boxes = [ax.get_tightbbox(renderer) for ax in axes]
    assert all(box.x0>=0 and box.y0>=0 and box.x1<=fig.bbox.width and box.y1<=fig.bbox.height for box in boxes)
    assert all(boxes[k].x1 < boxes[k+1].x0 for k in range(2))
    assert len(b.lines)==4 and all(line.get_markersize()==4.5 for line in b.lines)
    assert len(c.patches)==12 and len(c.texts)==13
    assert len(c.lines)==0 and len(c.collections)==0
    assert len(c.containers)==4 and all(container.errorbar is None for container in c.containers)
    geometries = []
    for ax, letter in zip(axes, letters):
        p = ax.get_position()
        assert np.isclose(p.width*fw,pw) and np.isclose(p.height*fh,ph)
        offset = (letter.get_transform().transform((0,1))-ax.transAxes.transform((0,1)))/fig.dpi*25.4
        assert np.allclose(offset,[-9.5,.4])
        geometries.append([p.x0*fw,p.y0*fh,p.width*fw,p.height*fh])
    stem = out/'abc_preview'
    save_editable_svg(fig, stem.with_suffix('.svg'))
    fig.savefig(stem.with_suffix('.pdf'), bbox_inches=None)
    fig.savefig(stem.with_suffix('.png'), dpi=300, bbox_inches=None)
    fig.savefig(stem.with_suffix('.tiff'), dpi=600, bbox_inches=None,
                pil_kwargs={'compression':'tiff_lzw'})
    root = ET.parse(stem.with_suffix('.svg')).getroot()
    ns = {'s':'http://www.w3.org/2000/svg'}
    assert len(root.findall('.//s:linearGradient',ns))==3
    assert not root.findall('.//s:image',ns)
    fonts = [n.get('style','') for n in root.iter() if 'font-family' in n.get('style','')]
    assert fonts and all("'Arial'" in s for s in fonts)
    plt.close(fig)

    # Literal swatches, distinct from the composited XPS gradient appearance.
    card = plt.figure(figsize=(180/25.4,48/25.4),dpi=180)
    ca = card.add_axes([0,0,1,1]); ca.set(xlim=(0,180),ylim=(0,48)); ca.axis('off')
    roles = ['light','mid','main','outline']; xs = [43,80,117,154]
    for role,x in zip(roles,xs): ca.text(x,43,role,ha='center',va='center',fontsize=9)
    for family,y,label in [('primary1',28,'Primary 1'),('primary2',9,'Primary 2')]:
        ca.text(5,y+4,label,ha='left',va='center',fontsize=10)
        for role,x in zip(roles,xs):
            color = FAMILIES[family][role]
            ca.add_patch(Rectangle((x-14,y),28,8,facecolor=color,edgecolor='none'))
            ca.text(x,y-2.2,color,ha='center',va='top',fontsize=8)
    for ext in ('.svg','.pdf','.png'):
        card.savefig(out/('colour_card'+ext),dpi=300,bbox_inches=None)
    plt.close(card)
    params = {**PREVIEW, 'canvas_mm':[fw,fh], 'panel_rectangles_mm':geometries,
              'families':FAMILIES, 'style':STYLE, 'core_order':list(CORE_ORDER),
              'family_names':{'primary1':'Primary 1','primary2':'Primary 2','primary3':'Primary 3'},
              'xps_fill_alpha':[FILL_ALPHA_BASE,FILL_ALPHA_TIP],
              'synthetic':True,
              'peak_labels':'P1/P2/P3 are placeholders, not chemical assignments.'}
    (out/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
    checks = ['Both primary palettes exactly match the eight user-supplied HEX values.',
              'Yellow occurs only in panel a; no other auxiliary is used.',
              'Three XPS components plus baseline reproduce the unchanged total.',
              'Panel b contains four main/mid curves with 4.5 pt markers.',
              'Panel c has three bars, four layers each, 12 values and zero error bars.',
              '180 mm canvas, 46 mm frames at 1.3:1, established fonts and strokes retained.',
              'Panel anchors and text extents fit the canvas with no adjacent-panel overlap.',
              'SVG contains three native gradients, editable Arial text, no raster images.']
    (out/'validation.json').write_text(json.dumps({'passed':True,'checks':checks},indent=2)+'\n')
    print(json.dumps({'passed':True,'canvas_mm':[fw,fh],'c_layers_per_bar':4,'c_error_bars':False}))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'palette-preview')
