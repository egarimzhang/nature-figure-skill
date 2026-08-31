"""Approved synthetic nine-panel chemistry preview, not experimental evidence.
Run: python preview_template.py OUTPUT_DIRECTORY
Fixtures are simulated. This preview writes only to OUTPUT_DIRECTORY.
"""
import sys
import shutil
import matplotlib
matplotlib.use('Agg')
from publication_colors import *
from publication_style import *

PREVIEW = {
    'figure_width_mm': STYLE['figure_width_mm'], 'plot_width_mm': STYLE['plot_width_mm'], 'aspect': STYLE['aspect'],
    'left_mm': 12.0, 'column_pitch_mm': STYLE['cell_pitch_mm'],
    'bottom_mm': STYLE['multirow_bottom_mm'], 'top_mm': STYLE['multirow_top_mm'], 'row_frame_gap_mm': STYLE['row_frame_gap_mm'],
    'marker_size_pt': STYLE['marker_size'], 'bar_width_data': 105.0,
    'temperature_limits': [180,820],
    'colourbar_width_mm': STYLE['colourbar_width_mm'], 'colourbar_gap_mm': STYLE['colourbar_gap_mm'], 'colourbar_tick_pad_pt': STYLE['colourbar_tick_pad'],
    'gc_window_min': [6.35,7.05], 'gc_highlight_alpha': 0.35,
    'gc_display_offset': 1.18,
}

import csv
import json
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch,Rectangle
from matplotlib.ticker import FixedLocator,FormatStrFormatter


def read_csv(path):
    return np.genfromtxt(path,delimiter=',',names=True,dtype=None,encoding='utf-8')


def percentage_axes(ax,label,xticks=(300,500,700)):
    ax.set(xlim=PREVIEW['temperature_limits'],ylim=(0,100),xticks=xticks,
           yticks=[0,25,50,75,100],xlabel=r'$T$ / K',ylabel=label)
    set_bar_padding(ax,xticks,PREVIEW['bar_width_data'])
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))


def legend_above(ax,handles=None,ncol=3,**kwargs):
    return ax.legend(handles=handles,loc='lower right',bbox_to_anchor=(1,1.025),
            frameon=False,ncol=ncol,fontsize=STYLE['text_font'],borderaxespad=0,
            handlelength=kwargs.pop('handlelength',1.2),handletextpad=kwargs.pop('handletextpad',.35),
            columnspacing=kwargs.pop('columnspacing',.7),borderpad=.1,**kwargs)


def preview(out, source_dir=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    data_dir=out/'source_data';data_dir.mkdir(exist_ok=True)
    source_dir=Path(source_dir) if source_dir is not None else Path(__file__).resolve().parent.parent/'assets'/'preview-data'
    for name in ('b_paired_trends.csv','c_stacked_replicates.npz','c_stacked_replicates.csv',
                 'g_cv.csv','h_temperature_xrd.npz','i_raman.csv'):
        src=source_dir/name;dest=data_dir/name
        if src.resolve()!=dest.resolve():shutil.copy2(src,dest)
    apply_publication_style()
    rng=np.random.default_rng(817103)
    fw=PREVIEW['figure_width_mm'];pw=PREVIEW['plot_width_mm'];ph=pw/PREVIEW['aspect']
    row_gap=PREVIEW['row_frame_gap_mm'];bottom=PREVIEW['bottom_mm']
    fh=bottom+3*ph+2*row_gap+PREVIEW['top_mm']
    row_bottoms=[bottom+2*(ph+row_gap),bottom+ph+row_gap,bottom]
    fig=plt.figure(figsize=(fw/25.4,fh/25.4),dpi=180)
    axes=[];panel_letters=[];legends=[]
    for idx in range(9):
        row,col=divmod(idx,3)
        left=PREVIEW['left_mm']+col*PREVIEW['column_pitch_mm']
        ax=fig.add_axes([left/fw,row_bottoms[row]/fh,pw/fw,ph/fh])
        style_axis(ax);axes.append(ax);panel_letters.append(add_panel_label(ax,chr(97+idx)))
    a,b,c,d,e,f,g,h,i=axes
    blue,red=FAMILIES['blue'],FAMILIES['red']

    # a: two GC traces, same retention scale, no horizontal separator.
    rt=np.linspace(0,10,2001)
    common=.03+sum(amp*np.exp(-.5*((rt-center)/sigma)**2)
                   for amp,center,sigma in [(.40,2.1,.085),(.71,4.3,.10),(.42,8.4,.09)])
    before=common+rng.normal(0,.0013,len(rt))
    new_peak=.66*np.exp(-.5*((rt-6.7)/.105)**2)
    after=common+new_peak+rng.normal(0,.0013,len(rt))
    window=PREVIEW['gc_window_min']
    highlight=Rectangle((window[0],.0),window[1]-window[0],2.02,
                         facecolor=red['main'],edgecolor='none',
                         alpha=PREVIEW['gc_highlight_alpha'],zorder=.5)
    a.add_patch(highlight)
    a.plot(rt,before,color=NEUTRALS['mid'],lw=STYLE['curve_width'])
    a.plot(rt,after+PREVIEW['gc_display_offset'],color=blue['main'],lw=STYLE['curve_width'])
    a.text(.4,.88,'Before',color=NEUTRALS['mid'])
    a.text(.4,2.06,'After',color=blue['main'])
    a.annotate('New peak',xy=(6.7,1.88),xytext=(6.7,2.25),ha='center',va='bottom',
               fontsize=STYLE['text_font'],color=NEUTRALS['dark'],
               arrowprops=dict(arrowstyle='->',lw=STYLE['axis_width'],color=NEUTRALS['dark'],shrinkA=1,shrinkB=2))
    a.set(xlim=(0,10),ylim=(-.07,2.48),xticks=[0,2,4,6,8,10],yticks=[],
          xlabel='Retention time / min',ylabel='Signal / a.u.')
    a.yaxis.set_minor_locator(NullLocator())
    np.savetxt(data_dir/'a_gc.csv',np.column_stack([rt,before,after,after+PREVIEW['gc_display_offset'],new_peak]),delimiter=',',
               header='retention_time_min,before_raw,after_raw,after_display_offset,added_synthetic_peak',comments='')

    # b: approved 4.5 pt paired curves with clearly different family trajectories.
    paired=read_csv(data_dir/'b_paired_trends.csv')
    paired=paired[np.isin(paired['object'],CORE_ORDER)]
    np.savetxt(data_dir/'b_paired_trends.csv',paired,fmt=['%.18g','%s','%d','%.18g'],delimiter=',',header=','.join(paired.dtype.names),comments='')
    for j,(name,marker) in enumerate(zip(CORE_ORDER,['o','s'])):
        for measure in (1,2):
            sel=paired[(paired['object']==name)&(paired['measurement']==measure)]
            color=FAMILIES[name]['main' if measure==1 else 'mid']
            b.plot(sel['temperature_K'],sel['response_percent'],color=color,lw=STYLE['curve_width'],
                   marker=marker,ms=STYLE['marker_size'],mfc=color if measure==1 else 'white',
                   mec=color,mew=STYLE['marker_edge'],ls='-' if measure==1 else '--',label=f'{chr(65+j)}{measure}')
    percentage_axes(b,'Response / %',xticks=[300,400,500,600,700])
    legends.append(b.legend(loc='lower center',bbox_to_anchor=(.5,1.03),ncol=4,
                frameon=False,fontsize=STYLE['text_font'],handlelength=1.05,handletextpad=.3,
                columnspacing=.7,borderaxespad=0,borderpad=.15,labelspacing=.65))

    # c: preserve approved stack replicates/means/errors, three values per bar.
    stack=np.load(data_dir/'c_stacked_replicates.npz')
    cool_levels=stack_levels('blue')
    means,cumulative,sd=stacked_bars(c,stack['temperature_K'],stack['replicates'],cool_levels,
                error_kind='sd',error_scope='cumulative',width=PREVIEW['bar_width_data'],labels=['I','II','III'],annotate=True)
    percentage_axes(c,'Fraction / %')
    set_percentage_axis(c,values=np.r_[cumulative.ravel()+sd.ravel(),cumulative.ravel()-sd.ravel()])
    legends.append(c.legend(loc='upper left',ncol=3,frameon=False,fontsize=STYLE['text_font'],
                        handlelength=1.1,handletextpad=.35,columnspacing=.7,borderpad=.2))

    # d: approved preview explicitly enables orange beside the two primary families.
    # This is a fixed QA recipe, not permission to add orange to future figures.
    energy=np.linspace(281.8,293.2,1001);baseline=.028
    specs=[('blue',288.6,.58,.61),('orange',286.7,.51,.42),('red',284.7,.64,.98)]
    components=[]
    for k,(family,center,sigma,height) in enumerate(specs):
        signal=height*np.exp(-.5*((energy-center)/sigma)**2);components.append(signal)
        gradient_peak(d,energy,baseline+signal,family,baseline=baseline)
        d.plot(energy,baseline+signal,color=FAMILIES[family]['outline'],lw=STYLE['curve_width'])
        d.text(center,baseline+height+.065,f'P{k+1}',ha='center',color=FAMILIES[family]['outline'])
    fit=baseline+np.sum(components,axis=0);raw=fit+rng.normal(0,.008,len(energy))
    d.plot(energy,fit,color=NEUTRALS['dark'],lw=STYLE['curve_width'],ls='--')
    d.plot(energy[::13],raw[::13],ls='none',marker='o',ms=2.2,mfc='none',mec='#969696',mew=.55,zorder=5)
    d.axhline(baseline,color=NEUTRALS['mid'],lw=STYLE['axis_width'],ls=':')
    d.set(xlim=(293.2,281.8),ylim=(0,1.28),xticks=[292,290,288,286,284,282],yticks=[0,.4,.8,1.2],
          xlabel='Binding energy / eV',ylabel='Intensity / a.u.')
    d.text(.03,.97,'XPS',transform=d.transAxes,va='top')
    np.savetxt(data_dir/'d_xps.csv',np.column_stack([energy,raw,fit,*components]),delimiter=',',
              header='binding_energy_eV,synthetic_observation,total,blue,orange,red',comments='')

    # e: monochrome selectivity bars and monochrome conversion point-line on independent y axes.
    temperatures=np.array([300,500,700]);selectivity=np.array([54,70,82]);conversion=np.array([28,55,88])
    for t,value in zip(temperatures,selectivity):
        gradient_bar(e,t,value,'blue',width=PREVIEW['bar_width_data'])
    percentage_axes(e,'Selectivity / %')
    right=make_twin_axis(e);right.set(ylim=(0,100),yticks=[0,25,50,75,100],ylabel='Conversion / %')
    right.plot(temperatures,conversion,color=red['main'],lw=STYLE['curve_width'],marker='o',ms=STYLE['marker_size'],mew=STYLE['marker_edge'])
    legends.append(legend_above(right,[Patch(facecolor=blue['mid'],label='S'),
                    Line2D([],[],color=red['main'],marker='o',ms=STYLE['marker_size'],lw=STYLE['curve_width'],label='X')],ncol=2))
    twin_width=fit_twin_to_width(e,right,target_right_mm=118)
    right_axis_mm=e.get_position().x1*fw
    np.savetxt(data_dir/'e_twin.csv',np.column_stack([temperatures,selectivity,conversion]),delimiter=',',
              header='temperature_K,selectivity_percent,conversion_percent',comments='')

    # f: six segment values per bar; total visual progression dark -> light -> dark.
    warm_levels=stack_levels('red',reverse=True)
    six_colors=cool_levels+warm_levels
    six_values=np.array([[13,12,13,12,13,12],[14,13,14,14,13,14],[15,16,15,16,15,16]],dtype=float)
    bottom_values=np.zeros(3)
    labels=['B1','B2','B3','R1','R2','R3']
    for j,(color,label) in enumerate(zip(six_colors,labels)):
        f.bar(temperatures,six_values[:,j],bottom=bottom_values,width=PREVIEW['bar_width_data'],
              facecolor=color,edgecolor='none',label=label,zorder=2)
        for t,value,base in zip(temperatures,six_values[:,j],bottom_values):
            f.text(t,base+value/2,f'{value:g}',ha='center',va='center',
                   color='white' if j==0 else NEUTRALS['dark'],fontsize=STYLE['text_font'],zorder=4)
        bottom_values+=six_values[:,j]
    percentage_axes(f,'Fraction / %')
    legends.append(legend_above(f,ncol=6,handlelength=.7,handletextpad=.2,columnspacing=.3))
    np.savetxt(data_dir/'f_six_segments.csv',np.column_stack([temperatures,six_values]),delimiter=',',
               header='temperature_K,B1,B2,B3,R1,R2,R3',comments='')

    # g: preserve previous CV loops; scan rate is the ordered blue lightness variable.
    cv=read_csv(data_dir/'g_cv.csv')
    cv_key='scan_rate_mV_s_or_reference'
    line_colors=[NEUTRALS['mid'],blue['mid'],blend(blue['mid'],blue['main'],.5),blue['main']]
    for key,color,label in zip(['reference','25','50','100'],line_colors,['Ref.','25','50','100']):
        sel=cv[cv[cv_key]==key]
        g.plot(sel['potential_V'],sel['schematic_current_density'],color=color,lw=STYLE['curve_width'],
               ls='--' if key=='reference' else '-',label=label)
    g.set(xlim=(-.24,.70),ylim=(-2.3,2.6),xticks=[-.2,0,.2,.4,.6],yticks=[-2,-1,0,1,2],
          xlabel=r'$E$ / V vs. RHE',ylabel=r'$j$ / mA cm$^{-2}$')
    handles,names=g.get_legend_handles_labels();order=[0,2,1,3]
    legends.append(g.legend([handles[k] for k in order],[names[k] for k in order],loc='upper left',ncol=2,
                            title=r'$v$ / mV s$^{-1}$',title_fontsize=STYLE['text_font'],handlelength=1.25,
                            handletextpad=.35,columnspacing=.65,labelspacing=.2,borderpad=.1))

    # h: use the ordinary panel b as the column reference, not the narrowed twin panel e.
    column_right_mm=b.get_position().x1*fw
    cbw=PREVIEW['colourbar_width_mm'];cbgap=PREVIEW['colourbar_gap_mm']
    hleft=h.get_position().x0*fw
    cax=add_aligned_colorbar_axis(h,reference_ax=b,width_mm=cbw,gap_mm=cbgap)
    xrd_width=h.get_position().width*fw
    xrd=np.load(data_dir/'h_temperature_xrd.npz')
    im=h.imshow(xrd['globally_normalized_intensity'],extent=(20,60,350,750),origin='lower',
                aspect='auto',interpolation='nearest',cmap=sequential_cmap('blue'),vmin=0,vmax=1,zorder=1)
    h.set(xlim=(20,60),ylim=(350,750),xticks=[20,30,40,50,60],yticks=[350,450,550,650,750],
          xlabel=r'$2\theta$ / °',ylabel=r'$T$ / K')
    h.text(.035,.97,'I → II',transform=h.transAxes,va='top')
    h.text(24,410,'I',ha='center');h.text(34,695,'II',ha='center')
    cb=fig.colorbar(im,cax=cax,ticks=[0,.5,1]);cb.set_ticklabels(['0','0.5','1']);cb.solids.set_rasterized(False);cb.solids.set_edgecolor('face')
    cb.outline.set_edgecolor(NEUTRALS['dark']);cb.outline.set_linewidth(STYLE['axis_width'])
    cax.tick_params(which='major',length=STYLE['major_length'],width=STYLE['axis_width'],
             pad=PREVIEW['colourbar_tick_pad_pt'],colors=NEUTRALS['dark'],labelsize=STYLE['axis_font'])
    cax.yaxis.set_minor_locator(FixedLocator([.25,.75]))
    cax.tick_params(which='minor',length=STYLE['minor_length'],width=STYLE['axis_width'],colors=NEUTRALS['dark'])
    cax.set_title(r'$I$ / a.u.',fontsize=STYLE['text_font'],pad=3)

    # i: previous offset Raman data, lower blue/upper coral, grey separator.
    raman=read_csv(data_dir/'i_raman.csv');shift=raman['raman_shift_cm1']
    for family,base in [('blue',.12),('red',2.42)]:
        fam=FAMILIES[family];shades=[fam['mid'],blend(fam['mid'],fam['main'],.5),fam['main']]
        for k,(temp,color) in enumerate(zip([300,400,500],shades)):
            yy=raman[f'{family}_{temp}K_display_offset']
            i.plot(shift,yy,color=color,lw=STYLE['curve_width'])
            i.text(790,base+.6*k+.09,f'{temp} K',ha='right',color=fam['outline'])
    i.axhline(2.05,color=NEUTRALS['mid'],lw=STYLE['axis_width'])
    i.set(xlim=(180,820),ylim=(0,4.25),xticks=[200,400,600,800],yticks=[],
          xlabel=r'Raman shift / cm$^{-1}$',ylabel='Intensity / a.u.')
    i.yaxis.set_minor_locator(NullLocator())
    i.text(220,1.78,'Primary 1',color=blue['outline']);i.text(220,4.13,'Primary 2',color=red['outline'],va='top')

    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    geometries=[];boxes=[]
    for idx,ax in enumerate(axes):
        position=ax.get_position();rect=np.array([position.x0*fw,position.y0*fh,position.width*fw,position.height*fh])
        parts=[ax.get_tightbbox(renderer)]
        if idx==4:parts.append(right.get_tightbbox(renderer))
        if idx==7:parts.append(cax.get_tightbbox(renderer))
        bb=mpl.transforms.Bbox.union(parts);boxes.append(bb)
        assert bb.x0>=0 and bb.x1<=fig.bbox.width and bb.y0>=0 and bb.y1<=fig.bbox.height, (idx,bb)
        assert abs(rect[3]-ph)<1e-6
        offset=(panel_letters[idx].get_transform().transform((0,1))-ax.transAxes.transform((0,1)))/fig.dpi*25.4
        assert np.allclose(offset,[-9.5,.4])
        geometries.append({'panel':chr(97+idx),'rectangle_mm':rect.tolist()})
    for row in range(3):
        assert np.ptp([axes[k].get_position().y0 for k in range(row*3,row*3+3)])<1e-9
        for k in range(row*3,row*3+2):
            if k==7:
                # The colourbar and panel i label share a gutter at different heights.
                # Check the actual text boxes rather than a union of empty corners.
                assert boxes[k].x1 < i.get_tightbbox(renderer,bbox_extra_artists=[]).x0
                next_letter=panel_letters[8].get_window_extent(renderer)
                h_text=[*h.texts,*h.get_xticklabels(),*h.get_yticklabels(),h.xaxis.label,h.yaxis.label,
                        cax.title,*cax.get_yticklabels()]
                assert all(not next_letter.overlaps(t.get_window_extent(renderer)) for t in h_text)
            else:
                assert boxes[k].x1<boxes[k+1].x0, f'Horizontal collision {k}'
    for col in range(3):
        for row in range(2):
            assert boxes[row*3+col].y0>boxes[(row+1)*3+col].y1, f'Vertical collision {row,col}'
    assert len(b.lines)==4 and all(line.get_markersize()==4.5 for line in b.lines)
    assert len(c.texts)==10 and len(f.texts)==19  # 9 / 18 values plus each panel label
    assert len(a.lines)==2  # no separator in GC
    assert abs(cax.bbox.x1-b.bbox.x1)<.01
    assert np.allclose(means,stack['segment_means']) and np.allclose(sd,stack['boundary_sd'])
    assert new_peak[np.argmin(abs(rt-6.7))]>.65
    assert abs(before[np.argmin(abs(rt-6.7))]-.03)<.01
    pad_left=(300-PREVIEW['bar_width_data']/2-PREVIEW['temperature_limits'][0])/640*pw
    parameters={**PREVIEW,'canvas_mm':[fw,fh],'axis_text_pt':8,'inplot_text_pt':7.5,'panel_letter_pt':12,
                'axis_width_pt':.75,'curve_width_pt':1.125,'panel_geometry':geometries,
                'bar_edge_padding_normal_mm':pad_left,'e_twin_width_mm':twin_width,
                'e_right_axis_mm':right_axis_mm,'b_right_frame_mm':column_right_mm,'h_alignment_reference':'b ordinary frame','h_colourbar_right_mm':cax.get_position().x1*fw,
                'h_plot_width_mm':xrd_width,'f_segment_colours_bottom_to_top':six_colors,
                'f_colour_rule':'Blue dark -> mid -> light; coral light -> mid -> dark.',
                'synthetic':True,'c_error_definition':'SD of cumulative matched replicate sums, n=4',
                'preview_only':True}
    (out/'parameters.json').write_text(json.dumps(parameters,indent=2)+'\n')
    stem=out/'nine_panel_review'
    save_editable_svg(fig,stem.with_suffix('.svg'))
    fig.savefig(stem.with_suffix('.pdf'),bbox_inches=None)
    fig.savefig(stem.with_suffix('.png'),dpi=300,bbox_inches=None)
    fig.savefig(stem.with_suffix('.tiff'),dpi=600,bbox_inches=None,pil_kwargs={'compression':'tiff_lzw'})
    ns={'s':'http://www.w3.org/2000/svg'};svg=ET.parse(stem.with_suffix('.svg')).getroot()
    assert len(svg.findall('.//s:linearGradient',ns))==6  # three XPS peaks + three selection bars
    assert len(svg.findall('.//s:image',ns))==1
    styles={el.get('style','') for el in svg.iter() if 'font-family' in el.get('style','')}
    assert styles and all("'Arial'" in s for s in styles)
    checks=['All nine panel frames preserve common row height and 12 mm gaps.',
            'Decorated panels fit canvas; adjacent content and gutter text do not collide.',
            'GC has two offset spectra, no separator, and one highlighted newly added peak.',
            'Four paired curves use main/mid and 4.5 pt markers.',
            'c retains its source stack means and cumulative SD; nine value labels.',
            'f has exactly 18 value labels and six specified blue/coral segment colours.',
            'h colourbar right border equals b ordinary frame; the narrowed e frame is not a reference.',
            'SVG uses editable Arial text and six native gradients; only XRD intensity is raster.']
    (out/'validation.json').write_text(json.dumps({'passed':True,'checks':checks},indent=2)+'\n')
    print(json.dumps({'canvas_mm':[fw,fh],'twin_width_mm':twin_width,'h_width_mm':xrd_width,
                      'colourbar_right_mm':column_right_mm,'panels':9}))
    plt.close(fig)
    return parameters


if __name__=='__main__':
    preview(sys.argv[1] if len(sys.argv)>1 else 'template-preview')
