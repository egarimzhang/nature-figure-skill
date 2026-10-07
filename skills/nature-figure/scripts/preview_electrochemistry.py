"""Synthetic nine-panel chemistry/electrochemistry styling test, not experimental evidence.
Run: python scripts/preview_electrochemistry.py OUTPUT_DIRECTORY
Only output files are written. IR difference reference, PDOS offsets, designated barrier
and impedance model are illustrative and explicitly exported; no fitting is performed.
"""
import sys,json,shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
from publication_colors import *
from publication_style import *

PREVIEW={
    'figure_width_mm':STYLE['figure_width_mm'],'left_mm':10.,'column_pitch_mm':STYLE['cell_pitch_mm'],
    'plot_width_mm':STYLE['plot_width_mm'],'aspect':STYLE['aspect'],
    'bottom_mm':10.5,'top_mm':13.,'row_gap_mm':STYLE['row_frame_gap_mm'],
    'ir_reference_V':.8,'ir_maximum_V':1.4,'ir_target_band_cm1':1660.,
    'xps_baseline':.028,'bar_width_data':105.,'fill_alpha':.65,
    'pdos_offsets':[0.,2.25],
    'reaction_state_energies_eV':[0.,.18,.05,-.30],
    'reaction_transition_energies_eV':[.65,1.20,.60],
    'designated_rate_controlling_step':2,
    'nyquist_parameters':{
        'primary1':{'Rs_ohm':8.,'Rct_ohm':90.,'C_F':.00012,'sigma':20.},
        'primary2':{'Rs_ohm':8.,'Rct_ohm':55.,'C_F':.00016,'sigma':13.}},
}


def read_csv(path):
    return np.genfromtxt(path,delimiter=',',names=True,dtype=None,encoding='utf-8')


def save_csv(path,columns,header):
    np.savetxt(path,np.column_stack(columns),delimiter=',',header=header,comments='')


def configure_colorbar(fig,im,cax,title,ticks,labels):
    cb=fig.colorbar(im,cax=cax,ticks=ticks)
    cb.set_ticklabels(labels);cb.solids.set_rasterized(False);cb.solids.set_edgecolor('face')
    cb.outline.set_linewidth(STYLE['axis_width']);cb.outline.set_edgecolor(NEUTRALS['dark'])
    cax.tick_params(which='major',length=STYLE['major_length'],width=STYLE['axis_width'],
                    labelsize=STYLE['axis_font'],pad=STYLE['colourbar_tick_pad'],colors=NEUTRALS['dark'])
    cax.yaxis.set_minor_locator(AutoMinorLocator(2))
    cax.tick_params(which='minor',length=STYLE['minor_length'],width=STYLE['axis_width'],colors=NEUTRALS['dark'])
    cax.set_title(title,fontsize=STYLE['text_font'],pad=3)
    return cb


def main(out,fixture_dir=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    data=out/'source_data';data.mkdir(exist_ok=True)
    source=Path(fixture_dir) if fixture_dir is not None else Path(__file__).resolve().parent.parent/'assets'/'preview-data'
    for name in ['b_paired_trends.csv','h_temperature_xrd.npz']:
        if (source/name).resolve()!=(data/name).resolve():shutil.copy2(source/name,data/name)
    apply_publication_style()
    fw=PREVIEW['figure_width_mm'];pw=PREVIEW['plot_width_mm'];ph=pw/PREVIEW['aspect']
    fh=PREVIEW['bottom_mm']+3*ph+2*PREVIEW['row_gap_mm']+PREVIEW['top_mm']
    fig=plt.figure(figsize=(fw/25.4,fh/25.4),dpi=180)
    axes=[];letters=[]
    for k in range(9):
        row,col=divmod(k,3)
        left=PREVIEW['left_mm']+col*PREVIEW['column_pitch_mm']
        bottom=PREVIEW['bottom_mm']+(2-row)*(ph+PREVIEW['row_gap_mm'])
        ax=fig.add_axes([left/fw,bottom/fh,pw/fw,ph/fh])
        style_axis(ax,categorical_x=k==6);axes.append(ax);letters.append(add_panel_label(ax,chr(97+k)))
    a,b,c,d,e,f,g,h,i=axes
    first,second=FAMILIES['primary1'],FAMILIES['primary2']

    # a: signed IR changes relative to the initial potential. Positive target growth is coral.
    wn=np.linspace(1200,1900,351);potential=np.linspace(.8,1.4,121)
    t=(potential-.8)/.6;xx=wn[None,:]
    growth=t[:,None]**1.2*np.exp(-.5*((xx-(1660-28*t[:,None]))/23)**2)
    loss=-.72*t[:,None]*np.exp(-.5*((xx-(1420+8*t[:,None]))/30)**2)
    delta=growth+loss
    delta/=np.max(np.abs(delta))
    ir_cax=add_aligned_colorbar_axis(a,reference_ax=d)
    ir=a.imshow(delta,origin='lower',extent=(1200,1900,.8,1.4),aspect='auto',
                interpolation='nearest',cmap=diverging_cmap(),norm=mpl.colors.TwoSlopeNorm(vmin=-1,vcenter=0,vmax=1))
    a.set(xlim=(1900,1200),ylim=(.8,1.4),xticks=[1800,1600,1400,1200],yticks=[.8,1.,1.2,1.4],
          xlabel=r'Wavenumber (cm$^{-1}$)',ylabel=r'$E$ (V vs. RHE)')
    set_x_minor_ticks_from_data(a,wn)
    a.text(.035,.97,'IR, ref. 0.8 V',transform=a.transAxes,va='top')
    a.annotate('Growth',xy=(1635,1.31),xytext=(1810,1.15),color=second['outline'],
                arrowprops=dict(arrowstyle='->',color=second['outline'],lw=STYLE['axis_width']))
    configure_colorbar(fig,ir,ir_cax,r'$\Delta A$',[-1,0,1],['−1','0','1'])
    np.savez_compressed(data/'a_ir_difference.npz',wavenumber_cm1=wn,potential_V=potential,
                        normalized_delta_absorbance=delta,reference_potential_V=.8,
                        normalization='one global max absolute difference')

    # b: three colours explicitly requested: primary 1, priority Primary 3 yellow, primary 2.
    energy=np.linspace(281.8,293.2,1001);base=PREVIEW['xps_baseline'];components=[]
    specs=[('primary1',288.6,.58,.61),('primary3',286.7,.51,.42),('primary2',284.7,.64,.98)]
    for k,(family,center,width,height) in enumerate(specs):
        signal=height*np.exp(-.5*((energy-center)/width)**2);components.append(signal)
        gradient_peak(b,energy,base+signal,family,baseline=base)
        b.plot(energy,base+signal,color=FAMILIES[family]['outline'])
        b.text(center,base+height+.065,f'P{k+1}',ha='center',color=FAMILIES[family]['outline'])
    total=base+np.sum(components,axis=0)
    raw=total+np.random.default_rng(817106).normal(0,.006,len(total))
    b.plot(energy,total,color=NEUTRALS['dark'],ls='--')
    b.plot(energy[::13],raw[::13],ls='none',marker='o',ms=2.2,mfc='none',mec='#969696',mew=.55,zorder=5)
    b.axhline(base,color=NEUTRALS['mid'],ls=':',lw=STYLE['axis_width'])
    b.set(xlim=(293.2,281.8),ylim=(0,1.28),xticks=[292,290,288,286,284,282],yticks=[],
          xlabel='Binding energy (eV)',ylabel='Intensity (a.u.)')
    set_x_minor_ticks_from_data(b,energy)
    b.yaxis.set_minor_locator(NullLocator());b.text(.035,.97,'XPS',transform=b.transAxes,va='top')
    save_csv(data/'b_xps.csv',[energy,raw,total,*components],
             'binding_energy_eV,synthetic_observation,total,primary1,primary3,primary2')

    # c: paired measurement styles remain separate from category identity.
    paired=read_csv(data/'b_paired_trends.csv');paired=paired[np.isin(paired['object'],CORE_ORDER)]
    np.savetxt(data/'b_paired_trends.csv',paired,fmt=['%.18g','%s','%d','%.18g'],delimiter=',',header=','.join(paired.dtype.names),comments='')
    for k,(family,marker) in enumerate(zip(CORE_ORDER,['o','s'])):
        for measure,role in enumerate(['main','mid'],start=1):
            rows=paired[(paired['object']==family)&(paired['measurement']==measure)];color=FAMILIES[family][role]
            c.plot(rows['temperature_K'],rows['response_percent'],color=color,marker=marker,
                   ms=STYLE['marker_size'],mew=STYLE['marker_edge'],mec=color,
                   mfc=color if measure==1 else 'white',ls='-' if measure==1 else '--',label=f'{chr(65+k)}{measure}')
    c.set(xlim=(180,820),ylim=(0,100),xticks=[300,400,500,600,700],yticks=[0,25,50,75,100],
          xlabel=r'$T$ (K)',ylabel='Response (%)')
    set_x_minor_ticks_from_data(c,paired['temperature_K'])
    c.legend(loc='lower center',bbox_to_anchor=(.5,1.03),ncol=4,frameon=False,
             handlelength=1.05,handletextpad=.3,columnspacing=.7,borderaxespad=0,borderpad=.1)

    # d: one closed CV cycle in acquisition order, fill enclosed by forward/reverse branches.
    E=np.linspace(-.2,.65,401);q=(E+.2)/.85;taper=np.sin(np.pi*q)
    forward=.18*E+taper*(.36+1.22*np.exp(-.5*((E-.30)/.105)**2))
    reverse=.18*E-taper*(.33+.92*np.exp(-.5*((E-.10)/.11)**2))
    forward[[0,-1]]=.18*E[[0,-1]];reverse[[0,-1]]=.18*E[[0,-1]]
    cvx=np.r_[E,E[::-1]];cvy=np.r_[forward,reverse[::-1]]
    d.fill(cvx,cvy,facecolor=first['light'],edgecolor='none',alpha=PREVIEW['fill_alpha'],zorder=1)
    d.plot(cvx,cvy,color=first['outline'],zorder=3)
    d.axhline(0,color=NEUTRALS['light'],lw=STYLE['axis_width'],zorder=0)
    d.set(xlim=(-.25,.70),ylim=(-1.35,1.85),xticks=[-.2,0,.2,.4,.6],yticks=[-1,0,1],
          xlabel=r'$E$ (V vs. RHE)',ylabel=r'$j$ (mA cm$^{-2}$)')
    set_x_minor_ticks_from_data(d,E)
    d.text(.04,.96,'Cycle 1',transform=d.transAxes,va='top')
    save_csv(data/'d_single_cv.csv',[cvx,cvy,np.r_[np.ones(len(E)),np.full(len(E),-1)]],
             'potential_V,schematic_current_density_mA_cm2,scan_direction')

    # e: grouped replicate-summary bars using the default scheme and sample SD.
    temps=np.array([300.,500.,700.]);barw=48.;shift=28.
    raw_first=np.array([[58,62,61],[69,73,71],[76,81,79]],float)
    raw_second=np.array([[43,47,45],[57,62,60],[68,73,71]],float)
    legend_handles=[]
    for family,raw,xshift,label in [('primary1',raw_first,-shift,'A'),('primary2',raw_second,shift,'B')]:
        for k,(x,values) in enumerate(zip(temps,raw)):
            result=summary_bar(e,x+xshift,values,family,width=barw,error_kind='sd',
                               label=label if k==0 else None)
            if k==0: legend_handles.append(result['legend_handle'])
    e.set(ylim=(0,100),xticks=temps,yticks=[0,25,50,75,100],xlabel=r'$T$ (K)',ylabel='Response (%)')
    set_bar_padding(e,np.r_[temps-shift,temps+shift],np.full(6,barw))
    set_x_minor_ticks_from_data(e,np.r_[temps-shift,temps+shift])
    e.legend(handles=legend_handles,loc='upper left',ncol=2,handlelength=1.2,
             handletextpad=.4,columnspacing=1.,borderpad=.2)
    save_csv(data/'e_grouped_raw_bars.csv',[temps,*raw_first.T,*raw_second.T],
             'temperature_K,A_rep1,A_rep2,A_rep3,B_rep1,B_rep2,B_rep3')

    # f: positive PDOS densities in two offset groups; not a spin-up/spin-down convention.
    erel=np.linspace(-6,3,901);pdos=[]
    specifications=[[(.85,-3.6,.62),(1.15,-1.55,.50),(.52,.8,.62)],[(.55,-3.2,.72),(1.30,-.85,.62),(.67,1.45,.56)]]
    for k,(family,offset,peaks) in enumerate(zip(CORE_ORDER,PREVIEW['pdos_offsets'],specifications)):
        density=sum(amp*np.exp(-.5*((erel-center)/width)**2) for amp,center,width in peaks);pdos.append(density)
        f.fill_between(erel,offset,offset+density,color=FAMILIES[family]['light'],alpha=PREVIEW['fill_alpha'],linewidth=0)
        f.plot(erel,offset+density,color=FAMILIES[family]['outline'])
        f.axhline(offset,color=NEUTRALS['light'],lw=STYLE['axis_width'])
        f.text(-5.7,offset+1.55,chr(65+k),color=FAMILIES[family]['outline'])
    f.axvline(0,color=NEUTRALS['mid'],ls='--',lw=STYLE['axis_width'])
    f.set(xlim=(-6,3),ylim=(-.10,4.2),xticks=[-6,-4,-2,0,2],yticks=[],
          xlabel=r'$(E-E_{\mathrm{F}})$ (eV)',ylabel='PDOS (a.u.)')
    set_x_minor_ticks_from_data(f,erel)
    f.yaxis.set_minor_locator(NullLocator())
    save_csv(data/'f_pdos.csv',[erel,pdos[0],pdos[1],pdos[0],pdos[1]+2.25],
             'energy_relative_EF_eV,primary1_raw,primary2_raw,primary1_display,primary2_display')

    # g: an illustrative energy profile with the explicitly designated second step.
    stable=np.array(PREVIEW['reaction_state_energies_eV']);ts=np.array(PREVIEW['reaction_transition_energies_eV'])
    path_x=[];path_y=[]
    for step in range(3):
        color=second['main'] if step==1 else first['main']
        x=np.linspace(2*step+.25,2*step+1.75,151);t=(x-x[0])/(x[-1]-x[0])
        up=stable[step]+(ts[step]-stable[step])*(1-np.cos(2*np.pi*np.minimum(t,.5)))/2
        down=stable[step+1]+(ts[step]-stable[step+1])*(1+np.cos(2*np.pi*np.maximum(t-.5,0)))/2
        y=np.where(t<=.5,up,down);g.plot(x,y,color=color)
        path_x.extend(x);path_y.extend(y)
    for k,y in enumerate(stable):g.plot([2*k-.25,2*k+.25],[y,y],color=first['main'])
    g.annotate('RDS (schem.)',xy=(3,1.2),xytext=(3,1.46),ha='center',color=second['outline'],
               arrowprops=dict(arrowstyle='->',color=second['outline'],lw=STYLE['axis_width']))
    g.annotate('',xy=(3.55,1.2),xytext=(3.55,.18),arrowprops=dict(arrowstyle='<->',color=second['outline'],lw=STYLE['axis_width']))
    g.text(3.72,.65,'1.02 eV',color=second['outline'])
    g.set(xlim=(-.55,6.6),ylim=(-.5,1.65),xticks=[0,2,4,6],xticklabels=['R','I1','I2','P'],
          yticks=[0,.5,1.,1.5],xlabel='Reaction coordinate',ylabel=r'$\Delta G$ (eV)')
    save_csv(data/'g_energy_states.csv',[np.arange(4),stable],'state_index,free_energy_eV')
    save_csv(data/'g_transition_states.csv',[np.arange(1,4),ts,ts-stable[:-1]],'step,transition_energy_eV,forward_barrier_eV')
    save_csv(data/'g_path_curve.csv',[path_x,path_y],'display_coordinate,illustrative_energy_eV')

    # h: XRD scalar intensity map, aligned to ordinary e, not any narrowed map.
    xrd=np.load(data/'h_temperature_xrd.npz');xrd_cax=add_aligned_colorbar_axis(h,reference_ax=e)
    xim=h.imshow(xrd['globally_normalized_intensity'],extent=(20,60,350,750),origin='lower',
                 aspect='auto',interpolation='nearest',cmap=sequential_cmap('primary1'),vmin=0,vmax=1)
    h.set(xlim=(20,60),ylim=(350,750),xticks=[20,30,40,50,60],yticks=[350,450,550,650,750],
          xlabel=r'$2\theta$ (°)',ylabel=r'$T$ (K)')
    set_x_minor_ticks_from_data(h,[20,60])
    h.text(.035,.97,'I → II',transform=h.transAxes,va='top')
    configure_colorbar(fig,xim,xrd_cax,r'$I$ (a.u.)',[0,1],['0','1'])

    # i: synthetic series Rs + parallel RC + Warburg, not a fit to observations.
    frequency=np.logspace(4,-2,85);omega=2*np.pi*frequency;zcurves=[]
    for k,(family,p) in enumerate(PREVIEW['nyquist_parameters'].items()):
        z=p['Rs_ohm']+p['Rct_ohm']/(1+1j*omega*p['Rct_ohm']*p['C_F'])+p['sigma']*(1-1j)/np.sqrt(omega)
        zcurves.append(z)
        i.plot(z.real,-z.imag,color=FAMILIES[family]['main'],label=chr(65+k),marker=['o','s'][k],
               markevery=7,ms=STYLE['marker_size'],mew=STYLE['marker_edge'],mfc='white',mec=FAMILIES[family]['main'])
    i.set(xlim=(0,195),ylim=(0,156),xticks=[0,50,100,150],yticks=[0,50,100,150],
          xlabel=r"$Z^{\prime}$ ($\Omega$)",ylabel=r"$-Z^{\prime\prime}$ ($\Omega$)")
    set_x_minor_ticks_from_data(i,np.r_[zcurves[0].real,zcurves[1].real])
    # (195/156)==1.25, so equal impedance scales retain the ordinary 1.25:1 frame.
    i.set_aspect('equal',adjustable='box');i.legend(loc='upper left',ncol=2,handlelength=1.4,columnspacing=.8)
    i.text(.06,.71,'High → low f',transform=i.transAxes)
    save_csv(data/'i_nyquist.csv',[frequency,zcurves[0].real,zcurves[0].imag,zcurves[1].real,zcurves[1].imag],
             'frequency_Hz,primary1_Zreal_ohm,primary1_Zimag_ohm,primary2_Zreal_ohm,primary2_Zimag_ohm')

    # Geometry, identity and export invariants; complement with rendered visual review.
    fig.canvas.draw();renderer=fig.canvas.get_renderer();geometries=[]
    for ax,letter in zip(axes,letters):
        p=ax.get_position();geometries.append([p.x0*fw,p.y0*fh,p.width*fw,p.height*fh])
        assert abs(p.height*fh-ph)<1e-6
        offset=(letter.get_transform().transform((0,1))-ax.transAxes.transform((0,1)))/fig.dpi*25.4
        assert np.allclose(offset,[STYLE['panel_dx_mm'],STYLE['panel_dy_mm']])
    for row in range(3):
        assert np.ptp([axes[k].get_position().y0 for k in range(row*3,row*3+3)])<1e-9
    for col in range(3):
        for row in range(2):
            upper=axes[row*3+col].get_tightbbox(renderer);lower=axes[(row+1)*3+col].get_tightbbox(renderer)
            assert upper.y0>lower.y1,('row collision',row,col)
    for ax in [*axes,ir_cax,xrd_cax]:
        bb=ax.get_tightbbox(renderer)
        assert bb.x0>=0 and bb.y0>=0 and bb.x1<=fig.bbox.width and bb.y1<=fig.bbox.height,(ax,bb)
    # Colourbar titles/ticks share gutters with neighbouring letters and axis labels.
    # Compare individual decorations instead of unions that include empty corners.
    def decorations(ax):
        artists=[*ax.texts,*ax.get_xticklabels(),*ax.get_yticklabels(),ax.xaxis.label,ax.yaxis.label,ax.title]
        artists=[v for v in artists if v.get_visible() and v.get_text().strip()]
        if ax.get_legend() is not None:artists.append(ax.get_legend())
        return artists
    panel_artists=[decorations(ax) for ax in axes]
    panel_artists[0]+=decorations(ir_cax);panel_artists[7]+=decorations(xrd_cax)
    for row in range(3):
        for col in range(2):
            k=row*3+col
            for left in panel_artists[k]:
                for right in panel_artists[k+1]:
                    overlap=mpl.transforms.Bbox.intersection(left.get_window_extent(renderer),right.get_window_extent(renderer))
                    assert overlap is None or min(overlap.width,overlap.height)<.5,('gutter collision',k,left,right)
    assert abs(ir_cax.bbox.x1-d.bbox.x1)<.01
    assert abs(xrd_cax.bbox.x1-e.bbox.x1)<.01
    assert len(c.lines)==4 and all(line.get_markersize()==4.5 for line in c.lines)
    assert len(e.patches)==6 and not any(line.get_marker()=='o' for line in e.lines)
    assert cvx[0]==cvx[-1] and cvy[0]==cvy[-1]
    assert np.allclose(delta[0],0) and delta.min()<0<delta.max()
    assert all(np.all(v>=0) for v in pdos)
    scale=i.transData.transform([[0,0],[1,0],[0,1]])
    assert np.isclose(np.linalg.norm(scale[1]-scale[0]),np.linalg.norm(scale[2]-scale[0]))
    stem=out/'nine_panel_review';save_editable_svg(fig,stem.with_suffix('.svg'))
    fig.savefig(stem.with_suffix('.pdf'),bbox_inches=None)
    fig.savefig(stem.with_suffix('.png'),dpi=300,bbox_inches=None)
    fig.savefig(stem.with_suffix('.tiff'),dpi=600,bbox_inches=None,pil_kwargs={'compression':'tiff_lzw'})
    svg=ET.parse(stem.with_suffix('.svg')).getroot();ns={'s':'http://www.w3.org/2000/svg'}
    assert len(svg.findall('.//s:linearGradient',ns))==9
    assert len(svg.findall('.//s:image',ns))==2
    fonts=[el.get('style','') for el in svg.iter() if 'font-family' in el.get('style','')]
    assert fonts and all("'Arial'" in style for style in fonts)
    params={**PREVIEW,'canvas_mm':[fw,fh],'style':STYLE,'primary':PRIMARY,
            'auxiliary_anchors':AUXILIARY_ANCHORS,'active_scheme':list(CORE_ORDER),
            'on_request_priority':list(AUXILIARY_ORDER),
            'panel_rectangles_mm':geometries,'ir_colorbar_right_mm':ir_cax.get_position().x1*fw,
            'ir_reference_panel':'d','xrd_colorbar_right_mm':xrd_cax.get_position().x1*fw,
            'xrd_reference_panel':'e','nyquist_equal_units':True,'synthetic':True,
            'pdos_convention':'positive density plus display offsets; not spin channels',
            'rds_convention':'illustratively designated second step; no kinetic inference',
            'nyquist_equation':'Z = Rs + Rct/(1+i*omega*Rct*C) + sigma*(1-i)/sqrt(omega)'}
    (out/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
    (out/'validation.json').write_text(json.dumps({'passed':True,'checks':[
        'Both colourbar right borders align to ordinary 1.25:1 frames (d/e).',
        'IR difference is zero at reference potential; zero-centred signed scale.',
        'XPS uses Primary 1/2 plus first on-request Primary 3 yellow.',
        'Four paired curves, one closed CV loop, and six grouped mean/SD gradient bars.',
        'Positive PDOS retained with documented display offsets and Fermi reference.',
        'Reaction energies and designated step exported; no fitted kinetic claim.',
        'Nyquist uses equal physical impedance scales and explicit analytic mock parameters.',
        'Fixed typography/geometry, nine native SVG gradients and two intentional raster maps.']},indent=2)+'\n')
    plt.close(fig);print(json.dumps({'passed':True,'canvas_mm':[fw,fh],'ir_colorbar_right_mm':params['ir_colorbar_right_mm'],'xrd_colorbar_right_mm':params['xrd_colorbar_right_mm']}))


if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else 'electrochemistry-preview')
