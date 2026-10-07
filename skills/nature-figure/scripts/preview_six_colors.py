"""Approved synthetic six-colour abcd preview, with all auxiliaries explicitly enabled in a.
Run: python scripts/preview_six_colors.py OUTPUT_DIRECTORY
"""
import sys,json,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from publication_colors import *
from publication_style import *

PREVIEW = {
    'canvas_width_mm':120., 'plot_width_mm':STYLE['plot_width_mm'], 'aspect':STYLE['aspect'],
    'left_mm':12., 'column_pitch_mm':STYLE['cell_pitch_mm'], 'bottom_mm':12.5, 'top_mm':7.,
    'row_frame_gap_mm':STYLE['row_frame_gap_mm'], 'bar_width_data':105.,
    'xps_baseline':.035, 'xps_rng_seed':817106,
    'xps_components':[
        ['primary1',292.0,.43,.42], ['cyan',290.3,.55,.55],
        ['blue',288.65,.50,.76], ['violet',287.0,.51,.50],
        ['primary3',285.35,.57,.65], ['primary2',283.65,.60,1.04]],
    'stack_roles_bottom_to_top':['outline','main','mid','light'],
    'raman_temperatures_K':[300,350,400,450,500,550],
    'raman_separator_y':3.95,
}


def read_csv(path):
    return np.genfromtxt(path,delimiter=',',names=True,dtype=None,encoding='utf-8')


def export(fig,stem):
    save_editable_svg(fig,stem.with_suffix('.svg'))
    fig.savefig(stem.with_suffix('.pdf'),bbox_inches=None)
    fig.savefig(stem.with_suffix('.png'),dpi=300,bbox_inches=None)
    fig.savefig(stem.with_suffix('.tiff'),dpi=600,bbox_inches=None,
                pil_kwargs={'compression':'tiff_lzw'})


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    data=out/'source_data';data.mkdir(exist_ok=True)
    src=Path(__file__).resolve().parent.parent/'assets'/'six-colour-preview-data'
    for name in ('b_two_objects.csv','c_values.csv','d_raman.csv'):
        if (src/name).resolve()!=(data/name).resolve():shutil.copy2(src/name,data/name)
    apply_publication_style()
    fw=PREVIEW['canvas_width_mm'];pw=PREVIEW['plot_width_mm'];ph=pw/PREVIEW['aspect']
    fh=PREVIEW['bottom_mm']+2*ph+PREVIEW['row_frame_gap_mm']+PREVIEW['top_mm']
    fig=plt.figure(figsize=(fw/25.4,fh/25.4),dpi=180)
    axes=[];letters=[]
    for k in range(4):
        row,col=divmod(k,2)
        left=PREVIEW['left_mm']+col*PREVIEW['column_pitch_mm']
        bottom=PREVIEW['bottom_mm']+(1-row)*(ph+PREVIEW['row_frame_gap_mm'])
        ax=fig.add_axes([left/fw,bottom/fh,pw/fw,ph/fh])
        style_axis(ax);axes.append(ax);letters.append(add_panel_label(ax,chr(97+k)))
    a,b,c,d=axes

    # a: six mock positive components; IDs are placeholders, not chemical assignments.
    energy=np.linspace(282.1,293.6,1501);baseline=PREVIEW['xps_baseline']
    components=[]
    for k,(family,center,sigma,height) in enumerate(PREVIEW['xps_components']):
        signal=height*np.exp(-.5*((energy-center)/sigma)**2);components.append(signal)
        gradient_peak(a,energy,baseline+signal,family,baseline=baseline)
        a.plot(energy,baseline+signal,color=FAMILIES[family]['outline'])
        a.text(center,baseline+height+.065,f'P{k+1}',ha='center',va='bottom',
               color=FAMILIES[family]['outline'],zorder=6)
    total=baseline+np.sum(components,axis=0)
    raw=total+np.random.default_rng(PREVIEW['xps_rng_seed']).normal(0,.005,len(energy))
    a.plot(energy,total,color=NEUTRALS['dark'],ls='--',zorder=4)
    a.plot(energy[::15],raw[::15],ls='none',marker='o',ms=2.2,mfc='none',
           mec='#969696',mew=.55,zorder=5)
    a.axhline(baseline,color=NEUTRALS['mid'],lw=STYLE['axis_width'],ls=':')
    a.set(xlim=(293.6,282.1),ylim=(0,1.34),xticks=[292,290,288,286,284],
          yticks=[0,.4,.8,1.2],xlabel='Binding energy (eV)',ylabel='Intensity (a.u.)')
    a.text(.03,.97,'XPS',transform=a.transAxes,va='top')
    np.savetxt(data/'a_xps.csv',np.column_stack([energy,raw,total,*components]),delimiter=',',
               header='binding_energy_eV,synthetic_observation,total,'+','.join(v[0] for v in PREVIEW['xps_components']),comments='')

    # b: preserve the earlier two-object/two-measurement data, alter colours only.
    paired=read_csv(data/'b_two_objects.csv')
    for j,(key,source_key,marker) in enumerate(zip(CORE_ORDER,['blue','red'],['o','s'])):
        for measure,role in enumerate(['main','mid'],start=1):
            rows=paired[(paired['object']==source_key)&(paired['measurement']==measure)]
            color=FAMILIES[key][role]
            b.plot(rows['temperature_K'],rows['response_percent'],color=color,marker=marker,
                   ms=STYLE['marker_size'],mew=STYLE['marker_edge'],mec=color,
                   mfc=color if measure==1 else 'white',ls='-' if measure==1 else '--',
                   label=f'{chr(65+j)}{measure}')
    b.set(xlim=(180,820),ylim=(0,100),xticks=[300,400,500,600,700],
          yticks=[0,25,50,75,100],xlabel=r'$T$ (K)',ylabel='Response (%)')
    b.legend(loc='lower center',bbox_to_anchor=(.5,1.03),ncol=4,frameon=False,
             handlelength=1.05,handletextpad=.3,columnspacing=.7,borderaxespad=0,borderpad=.1)

    # c: three bars with four solid components per bar, no uncertainties added.
    values=read_csv(data/'c_values.csv');temperatures=values['temperature_K']
    base=np.zeros(len(temperatures));stack_colors=stack_levels('primary1',count=4)
    for color,component in zip(stack_colors,['I','II','III','IV']):
        yy=values[component]
        c.bar(temperatures,yy,bottom=base,width=PREVIEW['bar_width_data'],
              color=color,edgecolor='none',label=component,zorder=2)
        rgb=np.asarray(mpl.colors.to_rgb(color))
        linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
        ink='white' if linear @ [.2126,.7152,.0722]<.25 else NEUTRALS['dark']
        for x,y,bottom in zip(temperatures,yy,base):
            c.text(x,bottom+y/2,f'{y:g}',ha='center',va='center',color=ink,zorder=4)
        base+=yy
    c.set(xticks=[300,500,700],yticks=[0,25,50,75,100],xlabel=r'$T$ (K)',ylabel='Fraction (%)')
    set_percentage_axis(c,values=base);set_bar_padding(c,temperatures,PREVIEW['bar_width_data'])
    c.legend(loc='upper left',ncol=4,frameon=False,handlelength=.9,
             handletextpad=.3,columnspacing=.6,borderpad=.2)

    # d: same twelve mock spectra, with documented vertical offsets unchanged.
    raman=read_csv(data/'d_raman.csv');raman_colors={}
    for family,source_key in zip(CORE_ORDER,['blue','red']):
        f=FAMILIES[family];raman_colors[family]=[]
        for k,temp in enumerate(PREVIEW['raman_temperatures_K']):
            rows=raman[(raman['family']==source_key)&(raman['temperature_K']==temp)]
            assert np.allclose(rows['raw_signal']+rows['display_offset'],rows['display_signal'])
            color=blend(f['mid'],f['outline'],k/5);raman_colors[family].append(color)
            d.plot(rows['raman_shift_cm1'],rows['display_signal'],color=color)
    d.axhline(PREVIEW['raman_separator_y'],color=NEUTRALS['mid'],lw=STYLE['axis_width'])
    d.set(xlim=(180,820),ylim=(0,8.2),xticks=[200,400,600,800],yticks=[],
          xlabel=r'Raman shift (cm$^{-1}$)',ylabel='Intensity (a.u.)')
    d.yaxis.set_minor_locator(NullLocator())
    d.text(205,3.78,'A',va='top',color=FAMILIES['primary1']['outline'])
    d.text(205,7.7,'B',color=FAMILIES['primary2']['outline'])
    d.text(.5,1.035,'300 → 550 K, step 50 K',transform=d.transAxes,ha='center',va='bottom')

    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    boxes=[ax.get_tightbbox(renderer) for ax in axes]
    assert all(bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height for bb in boxes)
    assert boxes[0].x1<boxes[1].x0 and boxes[2].x1<boxes[3].x0
    assert boxes[0].y0>boxes[2].y1 and boxes[1].y0>boxes[3].y1
    assert len(fig._publication_gradients)==6
    assert len(b.lines)==4 and all(line.get_markersize()==4.5 for line in b.lines)
    assert len(c.patches)==12 and len(c.texts)==13 and len(c.lines)==0 and len(c.collections)==0
    assert all(container.errorbar is None for container in c.containers)
    assert len(d.lines)==13
    geometries=[]
    for ax,letter in zip(axes,letters):
        p=ax.get_position();assert np.isclose(p.width*fw,pw) and np.isclose(p.height*fh,ph)
        offset=(letter.get_transform().transform((0,1))-ax.transAxes.transform((0,1)))/fig.dpi*25.4
        assert np.allclose(offset,[-9.5,.4])
        geometries.append([p.x0*fw,p.y0*fh,p.width*fw,p.height*fh])
    export(fig,out/'abcd_preview')
    root=ET.parse(out/'abcd_preview.svg').getroot();ns={'s':'http://www.w3.org/2000/svg'}
    assert len(root.findall('.//s:linearGradient',ns))==6 and not root.findall('.//s:image',ns)
    fonts=[e.get('style','') for e in root.iter() if 'font-family' in e.get('style','')]
    assert fonts and all("'Arial'" in s for s in fonts)
    plt.close(fig)

    # Separate literal swatches document the two ladders and four single anchors.
    card=plt.figure(figsize=(160/25.4,74/25.4),dpi=180)
    ax=card.add_axes([0,0,1,1]);ax.set(xlim=(0,160),ylim=(0,74));ax.axis('off')
    xs=[47,78,109,140];roles=['light','mid','main','outline']
    for x,role in zip(xs,roles):ax.text(x,69,role,ha='center',va='center',fontsize=9)
    for key,y,label in [('primary1',54,'Primary 1'),('primary2',35,'Primary 2')]:
        ax.text(4,y+4,label,ha='left',va='center',fontsize=9)
        for x,role in zip(xs,roles):
            color=FAMILIES[key][role]
            ax.add_patch(Rectangle((x-12,y),24,8,facecolor=color,edgecolor='none'))
            ax.text(x,y-2,color,ha='center',va='top',fontsize=8)
    ax.text(4,19,'On request',ha='left',va='center',fontsize=9)
    for x,(name,color) in zip(xs,AUXILIARY_ANCHORS.items()):
        ax.text(x,21,name.capitalize(),ha='center',va='center',fontsize=8)
        ax.add_patch(Rectangle((x-12,9),24,8,facecolor=color,edgecolor='none'))
        ax.text(x,7,color,ha='center',va='top',fontsize=8)
    for ext in ('.svg','.pdf','.png'):card.savefig(out/('colour_card'+ext),dpi=300,bbox_inches=None)
    plt.close(card)
    params={**PREVIEW,'canvas_mm':[fw,fh],'panel_rectangles_mm':geometries,
            'style':STYLE,'primary':PRIMARY,'auxiliary_anchors':AUXILIARY_ANCHORS,
            'auxiliary_outline':{n:FAMILIES[n]['outline'] for n in AUXILIARY_ANCHORS},
            'xps_gradient_alpha':[FILL_ALPHA_BASE,FILL_ALPHA_TIP],
            'xps_gradient_base_white_mix':.38,'auxiliary_outline_black_mix':.22,
            'raman_colors':raman_colors,'raman_temperature_direction':'bottom to top within each family',
            'c_error_bars':False,'synthetic':True,'preview_only':True}
    (out/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
    (out/'validation.json').write_text(json.dumps({'passed':True,'checks':[
        'Six positive XPS components, six native SVG gradients, no raster image.',
        'Two primary families; auxiliary colours appear only in a.',
        'Four main/mid point-lines, 4.5 pt markers; source values unchanged.',
        'Three bars with four literal layers and 12 numeric labels; no error bars.',
        'Twelve Raman spectra plus one grey separator, raw values and offsets preserved.',
        '46 mm frames at 1.3:1, 14 mm row and column gaps, Arial typography and physical panel anchors.',
        'Canvas bounds and adjacent panel envelopes do not collide.']},indent=2)+'\n')
    print(json.dumps({'passed':True,'canvas_mm':[fw,fh],'auxiliary_outlines':params['auxiliary_outline']}))


if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'palette-preview')
