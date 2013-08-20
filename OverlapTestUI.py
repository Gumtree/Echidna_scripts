# Script control setup area
__script__.title     = 'ECH Overlap'
__script__.version   = '1.0'

import sys

# Imports
from Reduction import overlap
'''Extra plots'''
if 'Plot4' not in globals():
    Plot4 = Plot(title='Chi-squared history')
    Plot4.close = noclose
if 'Plot5' not in globals():
    Plot5 = Plot(title='Gain')
    Plot5.close = noclose
if 'Plot6' not in globals():
    Plot6 = Plot(title='Residual Map')
    Plot6.close = noclose
''' User Interface '''

# Output Folder
out_folder = Par('file',"")
out_folder.dtype = 'folder'
output_xyd = Par('bool','True')
output_cif = Par('bool','True')
output_fxye = Par('bool','False')
output_stem = Par('string','overlap_')
Group('Output Folder').add(output_xyd,output_cif,output_fxye,output_stem,out_folder)

# Normalization
# We link the normalisation sources to actual dataset locations right here, right now
norm_table = {'Monitor 1':'bm1_counts','Monitor 2':'bm2_counts',
              'Monitor 3':'bm3_counts','Detector time':'detector_time'}
norm_apply     = Par('bool', 'True')
norm_reference = Par('string', 'Monitor 3', options = norm_table.keys())
norm_target    = Par('string', 'auto')
Group('Normalization').add(norm_apply, norm_reference, norm_target)

# Vertical Tube Correction
vtc_apply = Par('bool', 'True')
vtc_file  = Par('file', '')
vtc_file.ext = '*.txt,*.*'
Group('Vertical Tube Correction').add(vtc_apply, vtc_file)

# Efficiency Correction
eff_apply = Par('bool', 'True')
eff_map   = Par('file', '')
eff_map.ext = '*.*'
eff_show  = Act('eff_show_proc()', 'Show') 
Group('Efficiency Correction').add(eff_apply, eff_map, eff_show)

# Horizontal Tube Correction
#htc_apply = Par('bool', 'True')
#htc_file  = Par('file', '')
#htc_file.ext = '*.ang,*.*'
#Group('Horizontal Tube Correction').add(htc_apply, htc_file)

# Recalculate gain
regain_apply = Par('bool','True')
regain_iterno = Par('int','5')
regain_unit_weights = Par('bool','True')
regain_ignore = Par('int','2')
Group('Recalculate Gain').add(regain_apply,regain_iterno,regain_unit_weights,regain_ignore)

# Vertical Integration
vig_lower_boundary = Par('int', '0')
vig_upper_boundary = Par('int', '127')
#vig_apply_rescale  = Par('bool', 'True')
#vig_rescale_target = Par('float', '10000.0')
#vig_cluster = Par('float','0.03')
Group('Vertical Integration').add(vig_lower_boundary, vig_upper_boundary)

# Plot Helper
plh_from = Par('string', 'Plot 2', options = ['Plot 1', 'Plot 2', 'Plot 3'])
plh_to   = Par('string', 'Plot 3', options = ['Plot 1', 'Plot 2', 'Plot 3'])
plh_copy = Act('plh_copy_proc()', 'Copy')
Group('Copy 1D Datasets').add(plh_from, plh_to, plh_copy)

plh_plot    = Par('string', '', options = ['Plot 1', 'Plot 2', 'Plot 3'], command = 'plh_plot_changed()')
plh_dataset = Par('string', '', options = ['All'])
plh_delete  = Act('plh_delete_proc()', 'Delete')
Group('Delete 1D Datasets').add(plh_plot, plh_dataset, plh_delete)

''' Load Preferences '''

efficiency_file_uri     = __UI__.getPreference("au.gov.ansto.bragg.echidna.ui:efficiency_file_uri")
angular_offset_file     = __UI__.getPreference("au.gov.ansto.bragg.echidna.ui:angular_offset_file")
normalisation_reference = __UI__.getPreference("au.gov.ansto.bragg.echidna.ui:normalisation_reference")
user_output_dir         = __UI__.getPreference("au.gov.ansto.bragg.echidna.ui:user_output_dir")
#
# Set the optional values to those in the preferences file
#
if user_output_dir:
    out_folder.value = user_output_dir
if angular_offset_file:
    htc_file.value = angular_offset_file
if normalisation_reference:  #saved as location, need label instead
        vals = filter(lambda a:a[1]==normalisation_reference,norm_table.items())
        if vals: norm_reference.value = vals[0]
if efficiency_file_uri:
    eff_map.value = efficiency_file_uri

# Storage for efficiency map
if not 'eff_map_cache' in globals():
    eff_map_cache = {}
    
''' Button Actions '''

# show Efficiency Correction Map 
def eff_show_proc():
    from Reduction import reduction
    eff_map_canonical = eff_map.value
    if eff_map.value[0:5] != 'file:':
        eff_map_canonical = 'file:' + eff_map.value
    if not eff_map_canonical in eff_map_cache:
        eff_map_cache[eff_map_canonical] = reduction.read_efficiency_cif(eff_map_canonical)
    else:
        print 'Found in cache ' + `eff_map_cache[eff_map_canonical]`
    Plot1.clear()
    Plot1.set_dataset(eff_map_cache[eff_map_canonical][0])
    Plot1.title = 'Efficiency map'  #add info to this title!

def plh_copy_proc():
    
    src = str(plh_from.value)
    dst = str(plh_to.value)
    
    plots = {'Plot 1': Plot1, 'Plot 2': Plot2, 'Plot 3': Plot3}

    if not src in plots:
        print 'specify source plot'
        return
    if not dst in plots:
        print 'specify target plot'
        return
    if src == dst:
        print 'specify a different target plot'
        return
        
    src_plot = plots[src]
    dst_plot = plots[dst]
    
    src_ds = src_plot.ds
    if type(src_ds) is not list:
        print 'source plot does not contain 1D datasets'
        return
    
    dst_ds = dst_plot.ds
    if type(dst_ds) is not list:
        dst_plot.clear()
        dst_ds = []
    
    dst_ds_ids = [id(ds) for ds in dst_ds]
    
    for ds in src_ds:
        if id(ds) not in dst_ds_ids:
            dst_plot.add_dataset(ds)

def plh_plot_changed():
    
    target = str(plh_plot.value)
    
    plots = {'Plot 1': Plot1, 'Plot 2': Plot2, 'Plot 3': Plot3}
    
    if not target in plots:
        print 'specify source plot'
        plh_dataset.options = []
        return
    
    target_plot = plots[target]
    target_ds   = target_plot.ds
    target_list = ['All']
    
    if (type(target_ds) is not list) or (len(target_ds) == 0):
        print 'target plot does not contain 1D datasets'
        plh_dataset.options = []
        return
    
    for ds in target_ds:
        target_list.append(ds.title)
    
    plh_dataset.options = target_list
    plh_dataset.value   = 'All'

def plh_delete_proc():
    
    target  = str(plh_plot.value)
    dataset = str(plh_dataset.value)
    
    plots = {'Plot 1': Plot1, 'Plot 2': Plot2, 'Plot 3': Plot3}
    
    if not target in plots:
        print 'specify source plot'
        plh_dataset.options = []
        return
    
    target_plot = plots[target]
    target_ds   = target_plot.ds
    
    if (type(target_ds) is not list) or (len(target_ds) == 0):
        print 'target plot does not contain 1D datasets'
        plh_dataset.options = []
        return
    
    if dataset == 'All':
        for ds in target_ds:
            target_plot.remove_dataset(ds)
    else:
        for ds in target_ds:
            if ds.title == dataset:
                target_plot.remove_dataset(ds)

''' Script Actions '''

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    global Plot4,Plot5,Plot6
    from Reduction import reduction,AddCifMetadata
 
    from os.path import basename
    from os.path import join
    import time           #how fast are we going?
    from Formats import output
    
    elapsed = time.clock()
    print 'Started working at %f' % (time.clock()-elapsed)
    df.datasets.clear()
    
    # check input
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
        return

    # check if input needs to be normalized
    if norm_apply.value:
        # norm_ref is the source of information for normalisation
        # norm_tar is the value norm_ref should become,
        # by multiplication.  If 'auto', the maximum value of norm_ref
        # for the first dataset is used, otherwise any number may be entered.
        norm_ref = str(norm_reference.value)
        norm_tar = str(norm_target.value).lower()

        # check if normalization target needs to be determined
        if len(norm_tar) == 0:
            norm_ref = None
            norm_tar = None
            print 'WARNING: no reference for normalization was specified'
        elif norm_tar == 'auto':
            # set flag
            norm_tar = -1
            # iterate through input datasets
            location = norm_table[norm_ref]     
            print 'utilized reference value for "' + norm_ref + '" is:', norm_tar
            
        # use provided reference value
        else:
            norm_tar = float(norm_tar)
            
    else:
        norm_ref = None
        norm_tar = None

    # check if eff-map needs to be loaded
    if eff_apply.value:
        if not eff_map.value:
            eff = None
            print 'WARNING: no eff-map was specified'
        else:
            eff_map_canonical = str(eff_map.value)
            if eff_map_canonical[0:5] != 'file:':
                eff_map_canonical = 'file:' + eff_map_canonical
            if not eff_map_canonical in eff_map_cache:
                eff_map_cache[eff_map_canonical] = reduction.read_efficiency_cif(eff_map_canonical)
            else:
                print 'Found in cache ' + `eff_map_canonical`
        eff = eff_map_cache[eff_map_canonical]
    else:
        eff = None
    
    # check if vertical tube correction needs to be loaded
    if vtc_apply.value:
        if not vtc_file.value:
            vtc = None
            print 'WARNING: no vtc-file was specified'
        else:
            vtc = str(vtc_file.value)
    else:
        vtc = None
    
    # iterate through input datasets
    # note that the normalisation target (an arbitrary number) is set by
    # the first dataset unless it has already been specified.
    for fn in fns:
        # load dataset
        ds = df[fn]
        # extract basic metadata
        ds = reduction.AddCifMetadata.extract_metadata(ds)
        # remove redundant dimensions
        rs = ds.get_reduced()
        rs.copy_cif_metadata(ds)
        # check if normalized is required 
        if norm_ref:
            ds,norm_tar = reduction.applyNormalization(rs, reference=norm_table[norm_ref], target=norm_tar)
        
        print 'Finished normalisation at %f' % (time.clock()-elapsed)
        # check if vertical tube correction is required
        if vtc:
            ds = reduction.getVerticallyCorrected(ds, vtc)
        print 'Finished vertical offset correction at %f' % (time.clock()-elapsed)
        # check if efficiency correction is required
        if eff:
            ds = reduction.getEfficiencyCorrected(ds, eff)
        
        print 'Finished efficiency correction at %f' % (time.clock()-elapsed)
        # check if we are recalculating gain
        if regain_apply.value:
            b = ds.intg(axis=1).get_reduced()  #reduce dimension
            ignore = regain_ignore.value    #Ignore first two tubes
            # Determine pixels per tube interval
            tube_pos = ds.axes[-1]
            tubesep = abs(tube_pos[0]-tube_pos[-1])/(len(tube_pos)-1)
            tube_steps = ds.axes[0]
            bin_size = abs(tube_steps[0]-tube_steps[-1])/(len(tube_steps)-1)
            pixel_step = int(round(tubesep/bin_size))
            bin_size = tubesep/pixel_step
            print '%f tube separation, %d steps before overlap, ideal binsize %f' % (tubesep,pixel_step,bin_size)
            # Reshape with individual sections summed
            c = b.reshape([b.shape[0]/pixel_step,pixel_step,b.shape[-1]])
            print `b.shape` + "->" + `c.shape`
            # sum the individual unoverlapped sections
            d = c.intg(axis=1)
            e = d.transpose()
            # we skip the first tubes' data as it is all zero
            # Get an initial average to start with
            bottom = vig_lower_boundary.value
            top = vig_upper_boundary.value
            resummed = ds[:,bottom:top,:]
            resummed = resummed.intg(axis=1).get_reduced()
            first_gain = array.ones(len(b.transpose())-ignore)
            first_ave,x,first_var = overlap.apply_gain(resummed.transpose()[ignore:,:],1.0/resummed.transpose().var[ignore:,:],pixel_step,first_gain, calc_var=True)
            if regain_unit_weights.value is True:
                weights = array.ones_like(e[ignore:])
            else:
                weights = 1.0/e[ignore:].var
            q= iterate_data(e[ignore:],weights,pixel_step=1,iter_no=int(regain_iterno.value))
            # Now we actually apply the vertical limits requested
           
            f,x, varf = overlap.apply_gain(resummed.transpose()[ignore:,:],1.0/resummed.transpose().var[ignore:,:],pixel_step,q[0],calc_var=True)
            # Get error for full dataset
            esds = overlap.calc_error_new(b.transpose()[ignore:,:],f,q[0],pixel_step)
            f = Dataset(f)
            f.title = "After scaling"
            f.var = varf
            # construct the ideal axes
            axis = arange(len(f))
            f.axes[0] = axis*bin_size + ds.axes[0][0] + ignore*pixel_step*bin_size
            f.copy_cif_metadata(ds)
            print `f.shape` + ' ' + `x.shape`
            Plot1.set_dataset(f)
            first_ave = Dataset(first_ave)
            first_ave.var = first_var
            first_ave.title = "Before scaling"
            first_ave.axes[0] = f.axes[0]
            Plot1.add_dataset(Dataset(first_ave))
            Plot4.set_dataset(Dataset(q[4]))
            fg = Dataset(q[0])
            fg.var = esds
            Plot5.set_dataset(fg)
            # show old esds
            fgold = Dataset(q[0])
            fgold.var = q[5]
            Plot5.add_dataset(fgold)
            residual_map = Dataset(q[3])
            try:
                Plot6.set_dataset(residual_map)
            except:
                pass
        print 'Finished regain calculation at %f' % (time.clock() - elapsed)
        # Output datasets
        filename_base = join(str(out_folder.value),str(output_stem.value) + basename(str(fn))[:-7])
        if output_cif.value:
            output.write_cif_data(f,filename_base)
        if output_xyd.value:
            output.write_xyd_data(f,filename_base)
        if output_fxye.value:
            output.write_fxye_data(f,filename_base)
        print 'Finished writing data at %f' % (time.clock()-elapsed)

def iterate_data(dataset,weights,pixel_step=25,iter_no=5,pixel_mask=None):
    start_gain = array.ones(len(dataset))
    gain,first_ave,ar,esds,K = overlap.find_gain_fr(dataset,weights,pixel_step,start_gain,pixel_mask=pixel_mask)
    chisquared,residual_map = overlap.get_statistics_fr(gain,first_ave,dataset,dataset.var,pixel_step,pixel_mask)
    Plot1.set_dataset(Dataset(first_ave))
    Plot2.set_dataset(zeros_like(first_ave))
    old_result = first_ave    #store for later
    chisq_history = [chisquared]
    if iter_no > 0:
        no_iters = iter_no
    else:
        no_iters = abs(iter_no)
    for cycle_no in range(no_iters+1):
        esdflag = cycle_no == iter_no
        if cycle_no > 3 and iter_no < 0:
            esdflag = (esdflag or (abs(chisq_history[-2]-chisq_history[-1]))<0.005)
        gain,interim_result,ar,esds,K = overlap.find_gain_fr(dataset,weights,pixel_step,gain,arminus1=ar,pixel_mask=pixel_mask,errors=esdflag)
        chisquared,residual_map = overlap.get_statistics_fr(gain,interim_result,dataset,dataset.var,pixel_step,pixel_mask)
        chisq_history.append(chisquared)
        if not cycle_no % ((iter_no/2)+1):             # +1 to avoid division by zero for single step iterations
            print "Plotting cycle %d" % cycle_no
            Plot1.add_dataset(Dataset(interim_result))#,label="%d" % cycle_no)
            Plot2.add_dataset(Dataset(interim_result-first_ave))#,label="%d" % cycle_no)
            old_result = interim_result
            Plot3.set_dataset(Dataset(chisq_history))#,label="%d" % cycle_no)
    print 'Maximum shift/error: %f' % max(ar/esds)
    return gain,dataset,interim_result,residual_map,chisquared,esds,first_ave

# dispose
def __dispose__():
    global Plot1,Plot2,Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()


''' Quick-Fix '''

def run_action(act):
    act.set_running_status()
    try:
        exec(act.command)
        act.set_done_status()
    except:
        act.set_error_status()
        traceback.print_exc(file = sys.stdout)
        raise Exception, 'Error in running <' + act.text + '>'
