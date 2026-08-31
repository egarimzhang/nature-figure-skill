"""Synthetic a–i chemistry template QA, not experimental evidence.

Run: python preview_palette.py OUTPUT_DIRECTORY
All data, repeat measurements, peak positions and phase identities are illustrative.
In b/e, error bars are sample SDs of cumulative matched replicate sums (n=4).
This explicit auxiliary-colour QA recipe enables all five families in a/d,
including red+teal; b/f explicitly use orange. It is not a default palette extension.
"""
import sys
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Patch
from matplotlib.ticker import FixedLocator, FormatStrFormatter
from publication_colors import *
from publication_style import *

PLOT_HEIGHT_MM=STYLE['plot_width_mm']/STYLE['aspect']
ROW_GAP_MM=STYLE['row_frame_gap_mm']
BOTTOM_MM=STYLE['multirow_bottom_mm']
FIGURE_MM=(180.0,BOTTOM_MM+3*PLOT_HEIGHT_MM+2*ROW_GAP_MM+STYLE['multirow_top_mm'])
ROW_BOTTOM_MM=[BOTTOM_MM+k*(PLOT_HEIGHT_MM+ROW_GAP_MM) for k in (2,1,0)]
XRD_PLOT_WIDTH_MM=46.0-STYLE['colourbar_width_mm']-STYLE['colourbar_gap_mm']
RNG_SEED=73021


def legend_above(ax,handles=None,ncol=3):
    return ax.legend(handles=handles,loc='lower right',bbox_to_anchor=(1,1.025),
                     ncol=ncol,fontsize=STYLE['text_font'],borderaxespad=0,
                     handlelength=1.25,handletextpad=.35,columnspacing=.7,borderpad=.1)


def replicate_stacks(means,rng):
    """Four matched mock repeats with correlated component fluctuations."""
    means=np.asarray(means,dtype=float)
    fluct=rng.normal(0,1.25,size=(4,*means.shape))
    shared=rng.normal(0,.55,size=(4,means.shape[0],1))
    fluct+=shared
    fluct-=fluct.mean(axis=0,keepdims=True)
    return means[None,:,:]+fluct


def configure_percent(ax):
    ax.set(xlim=(180,820),ylim=(0,100),xticks=[300,500,700],yticks=[0,25,50,75,100],xlabel=r'$T$ / K')
    set_bar_padding(ax,[300,500,700],105)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))


def preview(out):
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    data_dir=out/'source_data';data_dir.mkdir(exist_ok=True)
    apply_publication_style()
    rng=np.random.default_rng(RNG_SEED)
    fw,fh=FIGURE_MM
    fig=plt.figure(figsize=(fw/25.4,fh/25.4),dpi=180)
    axes=[];letters=[];legends=[]
    for index,label in enumerate('abcdefghi'):
        row,col=divmod(index,3)
        left=12+60*col
        width=XRD_PLOT_WIDTH_MM if label=='h' else 46.0
        ax=fig.add_axes([left/fw,ROW_BOTTOM_MM[row]/fh,width/fw,PLOT_HEIGHT_MM/fh])
        style_axis(ax)
        axes.append(ax)
        letters.append(add_panel_label(ax,label))
    a,b,c,d,e,f,g,h,i=axes

    # a: all five explicit families and their roles; outline is the renamed line role.
    a.set(xlim=(0,46),ylim=(0,PLOT_HEIGHT_MM))
    names=list(CORE_ORDER)+list(AUXILIARY_ORDER)
    roles=['outline','main','mid','light']
    for k,role in enumerate(roles):
        a.text(14+8*k+3.35,34.0,role.capitalize(),ha='center',va='center',fontsize=STYLE['text_font'])
    for row,name in enumerate(names):
        yy=28.5-5.6*row
        title={'blue':'Primary 1','red':'Primary 2','orange':'Orange'}.get(name,name.capitalize())
        role='core' if name in CORE_ORDER else 'on request'
        a.text(0,yy,title+'\n'+role,ha='left',va='center',fontsize=STYLE['text_font'],linespacing=.92)
        for k,r in enumerate(roles):
            a.add_patch(Rectangle((14+8*k,yy-2),6.7,4,facecolor=FAMILIES[name][r],edgecolor='none'))
    a.axis('off')

    # b: three colours; uncertainty belongs to the cumulative boundaries, not isolated segments.
    temperatures=np.array([300,500,700])
    b_reps=replicate_stacks([[23,24,22],[33,25,22],[43,28,21]],rng)
    mean,boundary,err=stacked_bars(b,temperatures,b_reps,category_colors(3,'mid',families=['blue','red','orange']),
                                  error_kind='sd',error_scope='cumulative',width=105,
                                  labels=['A','B','C'])
    configure_percent(b);b.set_ylabel('Fraction / %')
    set_percentage_axis(b,values=np.r_[boundary.ravel()-err.ravel(),boundary.ravel()+err.ravel()])
    legends.append(legend_above(b))
    np.savez_compressed(data_dir/'b_stacked_replicates.npz',temperature_K=temperatures,replicates=b_reps,
                        segment_means=mean,boundary_means=boundary,boundary_sd=err)

    # c: two objects, two paired measurements. Hue = object; light/open = measurement 2.
    t=np.array([300,400,500,600,700])
    paired=[]
    markers=['o','s','^']
    for j,name in enumerate(CORE_ORDER):
        m1=np.array([16,26,43,61,77])+j*6
        m2=m1-np.array([5,4,6,5,7])
        for k,y in enumerate((m1,m2)):
            color=FAMILIES[name]['main' if k==0 else 'mid']
            c.plot(t,y,color=color,lw=STYLE['curve_width'],marker=markers[j],ms=STYLE['marker_size'],
                   mfc=color if k==0 else 'white',mec=color,mew=STYLE['marker_edge'],
                   linestyle='-' if k==0 else '--',label=f'{chr(65+j)}{k+1}')
            paired.extend(zip(t,[name]*len(t),[k+1]*len(t),y))
    c.set(xlim=(180,820),ylim=(0,100),xticks=t,yticks=[0,25,50,75,100],xlabel=r'$T$ / K',ylabel='Response / %')
    legends.append(c.legend(loc='upper left',ncol=3,handlelength=1.3,handletextpad=.35,columnspacing=.65,borderpad=.15,labelspacing=.2))
    with (data_dir/'c_paired_measurements.csv').open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['temperature_K','object','measurement','response_percent']);writer.writerows(paired)

    # d: five-component positive XPS-like signal; no actual chemical assignments.
    energy=np.linspace(282,294,1001);baseline=.028
    peak_specs=[('blue',292.0,.40,.40),('teal',289.8,.43,.54),('violet',288.2,.43,.36),
                ('orange',286.55,.46,.55),('red',284.7,.54,.96)]
    peaks=[]
    for k,(family,center,sigma,height) in enumerate(peak_specs):
        y=height*np.exp(-.5*((energy-center)/sigma)**2)
        peaks.append(y)
        gradient_peak(d,energy,baseline+y,family,baseline=baseline)
        d.plot(energy,baseline+y,color=FAMILIES[family]['outline'],lw=STYLE['curve_width'])
        d.text(center,baseline+height+.065,f'P{k+1}',ha='center',va='bottom',color=FAMILIES[family]['outline'])
    fit=baseline+np.sum(peaks,axis=0)
    raw=fit+rng.normal(0,.008,len(energy))
    d.plot(energy,fit,color=NEUTRALS['dark'],ls='--',lw=STYLE['curve_width'])
    d.plot(energy[::13],raw[::13],ls='none',marker='o',ms=2.2,mfc='none',mec='#969696',mew=.55,zorder=6)
    d.axhline(baseline,color=NEUTRALS['mid'],ls=':',lw=STYLE['axis_width'])
    d.set(xlim=(294,282),ylim=(0,1.26),xticks=[294,291,288,285,282],yticks=[0,.4,.8,1.2],
          xlabel='Binding energy / eV',ylabel='Intensity / a.u.')
    d.text(.03,.97,'XPS',transform=d.transAxes,va='top')
    np.savetxt(data_dir/'d_xps.csv',np.column_stack([energy,raw,fit,*peaks]),delimiter=',',
               header='binding_energy_eV,synthetic_observation,total,blue,teal,violet,orange,red',comments='')

    # e: three related blue depths. Three segment means are printed on EACH bar.
    e_reps=replicate_stacks([[21,24,23],[28,28,27],[32,30,28]],rng)
    blue=FAMILIES['blue']
    e_colors=stack_levels('blue')
    mean,boundary,err=stacked_bars(e,temperatures,e_reps,e_colors,error_kind='sd',
                                  error_scope='cumulative',width=105,labels=['I','II','III'],annotate=True)
    configure_percent(e);e.set_ylabel('Fraction / %')
    set_percentage_axis(e,values=np.r_[boundary.ravel()-err.ravel(),boundary.ravel()+err.ravel()])
    legends.append(legend_above(e))
    np.savez_compressed(data_dir/'e_stacked_replicates.npz',temperature_K=temperatures,replicates=e_reps,
                        segment_means=mean,boundary_means=boundary,boundary_sd=err)

    # f: two selectivities as grouped bars, conversion as one point-line on right y axis.
    selectivity=np.array([[22,38],[35,48],[42,51]])
    for j,family in enumerate(('blue','red')):
        for xx,value in zip(temperatures+(j-.5)*48,selectivity[:,j]):
            gradient_bar(f,xx,value,family,width=42)
    configure_percent(f);f.set_ylabel('Selectivity / %')
    right=make_twin_axis(f)
    right.set(ylim=(0,100),yticks=[0,25,50,75,100],ylabel='Conversion / %')
    conversion=np.array([42,65,89])
    right.plot(temperatures,conversion,color=FAMILIES['orange']['main'],marker='o',lw=STYLE['curve_width'],
               ms=STYLE['marker_size'],mew=STYLE['marker_edge'])
    f_handles=[Patch(facecolor=FAMILIES[n]['mid'],label=lab) for n,lab in [('blue','S1'),('red','S2')]]
    f_handles.append(Line2D([],[],color=FAMILIES['orange']['main'],marker='o',ms=STYLE['marker_size'],label='X'))
    legends.append(legend_above(right,f_handles))
    twin_width=fit_twin_to_width(f,right,target_right_mm=178)
    np.savetxt(data_dir/'f_twin.csv',np.column_stack([temperatures,selectivity,conversion]),delimiter=',',
               header='temperature_K,selectivity_1_percent,selectivity_2_percent,conversion_percent',comments='')

    # g: CV loops, ordered blue shades for scan rate, grey reference loop.
    potential=np.linspace(-.2,.65,401)
    phase=(potential+.2)/.85
    taper=np.sin(np.pi*phase)
    def loop(rate,amplitude=1):
        v=rate/50
        background=.28*potential
        up=background+amplitude*(.25*v*taper+1.30*np.sqrt(v)*np.exp(-.5*((potential-.34)/.077)**2))
        down=background-amplitude*(.25*v*taper+1.05*np.sqrt(v)*np.exp(-.5*((potential-.17)/.082)**2))
        # Enforce matching switching/end currents without artificial jumps.
        for q in (up,down): q[0]=background[0];q[-1]=background[-1]
        return np.r_[potential,potential[::-1]],np.r_[up,down[::-1]]
    cv_rows=[]
    ep,ref=loop(50,.34)
    g.plot(ep,ref,color=NEUTRALS['mid'],lw=STYLE['curve_width'],ls='--',label='Ref.')
    cv_rows.extend(zip(ep,ref,['reference']*len(ep)))
    rate_colors=[blue['mid'],blend(blue['mid'],blue['main'],.5),blue['main']]
    for rate,color in zip([25,50,100],rate_colors):
        ep,current=loop(rate)
        g.plot(ep,current,color=color,lw=STYLE['curve_width'],label=str(rate))
        cv_rows.extend(zip(ep,current,[str(rate)]*len(ep)))
    g.set(xlim=(-.24,.70),ylim=(-2.3,2.6),xticks=[-.2,0,.2,.4,.6],yticks=[-2,-1,0,1,2],
          xlabel=r'$E$ / V vs. RHE',ylabel=r'$j$ / mA cm$^{-2}$')
    cv_handles,cv_labels=g.get_legend_handles_labels()
    legends.append(g.legend([cv_handles[k] for k in [0,2,1,3]],[cv_labels[k] for k in [0,2,1,3]],loc='upper left',ncol=2,title=r'$v$ / mV s$^{-1}$',title_fontsize=7.5,
                            handlelength=1.25,handletextpad=.35,columnspacing=.65,labelspacing=.2,borderpad=.1))
    with (data_dir/'g_cv.csv').open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['potential_V','schematic_current_density','scan_rate_mV_s_or_reference']);writer.writerows(cv_rows)

    # h: temperature-programmed XRD intensity map with a schematic I -> II transition.
    angle=np.linspace(20,60,601);temperature=np.linspace(350,750,161)
    xx,tt=np.meshgrid(angle,temperature)
    fraction=1/(1+np.exp(-(tt-545)/24))
    def peak(center,width): return np.exp(-.5*((xx-center)/width)**2)
    intensity=.025+(1-fraction)*(peak(27.2-.0008*(tt-350),.26)+.7*peak(40.5-.0007*(tt-350),.30))
    intensity+=fraction*(.92*peak(31.7-.0006*(tt-350),.29)+.72*peak(46.8-.0005*(tt-350),.32))
    intensity+=.18*peak(55.3,.27)
    intensity=np.maximum(0,intensity+rng.normal(0,.007,intensity.shape))
    intensity/=intensity.max()  # one global normalization, not per temperature slice
    cax=add_aligned_colorbar_axis(h,reference_ax=e)  # e is an ordinary, unshortened frame here
    im=h.imshow(intensity,extent=(20,60,350,750),origin='lower',aspect='auto',interpolation='nearest',
                cmap=sequential_cmap('blue'),vmin=0,vmax=1,zorder=1)
    h.set(xlim=(20,60),ylim=(350,750),xticks=[20,30,40,50,60],yticks=[350,450,550,650,750],
          xlabel=r'$2\theta$ / °',ylabel=r'$T$ / K')
    h.text(.03,.97,'I → II',transform=h.transAxes,va='top')
    h.text(24,410,'I',ha='center');h.text(34,695,'II',ha='center')
    cb=fig.colorbar(im,cax=cax,ticks=[0,.5,1]);cb.set_ticklabels(['0','0.5','1'])
    cb.solids.set_rasterized(False)
    cb.solids.set_edgecolor("face")  # avoid vector cell seams in SVG/PDF viewers
    cb.outline.set_linewidth(STYLE['axis_width']);cb.outline.set_edgecolor(NEUTRALS['dark'])
    cax.tick_params(which='major',length=STYLE['major_length'],width=STYLE['axis_width'],
                     pad=STYLE['colourbar_tick_pad'],colors=NEUTRALS['dark'],labelsize=STYLE['axis_font'])
    cax.yaxis.set_minor_locator(FixedLocator([.25,.75]))
    cax.tick_params(which='minor',length=STYLE['minor_length'],width=STYLE['axis_width'],colors=NEUTRALS['dark'])
    cax.set_title(r'$I$ / a.u.',fontsize=STYLE['text_font'],pad=3)
    np.savez_compressed(data_dir/'h_temperature_xrd.npz',two_theta_deg=angle,temperature_K=temperature,
                        globally_normalized_intensity=intensity,illustrative_phase_II_fraction=fraction[:,0])

    # i: blue below, coral above, separated by a grey line. Offsets are display-only.
    shift=np.linspace(200,800,901);raman_columns=[shift];raman_headers=['raman_shift_cm-1']
    for family,offset_base in [('blue',.12),('red',2.42)]:
        fam=FAMILIES[family]
        shade=[fam['mid'],blend(fam['mid'],fam['main'],.5),fam['main']]
        for k,temp in enumerate([300,400,500]):
            centers=(320-3*k,598+2*k) if family=='blue' else (422-3*k,653+2*k)
            signal=(.39+.035*k)*np.exp(-.5*((shift-centers[0])/17)**2)
            signal+=(.28+.015*k)*np.exp(-.5*((shift-centers[1])/23)**2)
            offset=offset_base+.6*k
            i.plot(shift,signal+offset,color=shade[k],lw=STYLE['curve_width'])
            i.text(790,offset+.09,f'{temp} K',ha='right',color=fam['outline'])
            raman_columns += [signal,signal+offset]
            raman_headers += [f'{family}_{temp}K_raw',f'{family}_{temp}K_display_offset']
    i.axhline(2.05,color=NEUTRALS['mid'],lw=STYLE['axis_width'])
    i.set(xlim=(180,820),ylim=(0,4.25),xticks=[200,400,600,800],yticks=[],
          xlabel=r'Raman shift / cm$^{-1}$',ylabel='Intensity / a.u.')
    i.yaxis.set_minor_locator(NullLocator())
    i.text(220,1.78,'Primary 1',color=blue['outline']);i.text(220,4.13,'Primary 2',color=FAMILIES['red']['outline'],va='top')
    np.savetxt(data_dir/'i_raman.csv',np.column_stack(raman_columns),delimiter=',',header=','.join(raman_headers),comments='')

    # Numeric invariants plus renderer-dependent geometry. Visual QA remains required.
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    geometry=[]
    for idx,ax in enumerate(axes):
        p=ax.get_position();rect=np.array([p.x0*fw,p.y0*fh,p.width*fw,p.height*fh])
        bb=ax.get_tightbbox(renderer)
        if bb.x0 < -1 or bb.y0 < -1 or bb.x1>fig.bbox.width+1 or bb.y1>fig.bbox.height+1:
            raise AssertionError(f'Panel {chr(97+idx)} decorated bounds escape canvas: {bb}')
        assert abs(rect[3]-PLOT_HEIGHT_MM)<1e-7
        loc=letters[idx].get_transform().transform((0,1))
        anchor=ax.transAxes.transform((0,1))
        assert np.allclose((loc-anchor)/fig.dpi*25.4,[-9.5,.4])
        geometry.append(dict(panel=chr(97+idx),rect_mm=rect.tolist(),decorated_bbox_px=list(bb.bounds)))
    assert len(c.lines)==4 and all(line.get_markersize()==STYLE['marker_size'] for line in c.lines)
    assert abs(cax.bbox.x1-e.bbox.x1)<.01
    assert len(e.texts)==10  # 9 segment labels + panel letter
    for row in range(3):
        assert np.ptp([ax.get_position().y0 for ax in axes[row*3:row*3+3]])<1e-10
    right_bound=max(x.get_tightbbox(renderer).x1 for x in (f,right))/fig.dpi*25.4
    assert abs(right_bound-178)<.05
    parameters=dict(style=STYLE,canvas_mm=FIGURE_MM,plot_height_mm=PLOT_HEIGHT_MM,
                    panel_geometry=geometry,twin_plot_width_mm=twin_width,
                    twin_decorated_right_mm=right_bound,xrd_plot_width_mm=XRD_PLOT_WIDTH_MM,
                    fill_alpha=[FILL_ALPHA_BASE,FILL_ALPHA_TIP],bar_mid={n:FAMILIES[n]['mid'] for n in CORE_ORDER},
                    role_rename='line -> outline (line retained only as deprecated compatibility alias)',
                    synthetic=True,stack_error='SD of cumulative matched replicate sums, n=4',
                    xrd_note='Global normalization; phases I/II illustrative; not evidence of a surface-specific phase transition.',
                    raman_note='Each curve has a documented additive display offset; raw signals exported.')
    (out/'parameters.json').write_text(json.dumps(parameters,indent=2)+'\n')
    stem=out/'nine_panel_template'
    save_editable_svg(fig,stem.with_suffix('.svg'))
    fig.savefig(stem.with_suffix('.pdf'),bbox_inches=None)
    fig.savefig(stem.with_suffix('.png'),dpi=300,bbox_inches=None)
    fig.savefig(stem.with_suffix('.tiff'),dpi=600,bbox_inches=None,pil_kwargs={'compression':'tiff_lzw'})
    print(json.dumps({'canvas_mm':FIGURE_MM,'twin_width_mm':twin_width,'twin_right_mm':right_bound,'panels':9}))
    plt.close(fig)
    return parameters


if __name__=='__main__':
    preview(sys.argv[1] if len(sys.argv)>1 else 'template-preview')
