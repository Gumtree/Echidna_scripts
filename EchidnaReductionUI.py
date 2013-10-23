# Script control setup area
__script__.title     = 'ECH Reduction'
__script__.version   = '1.0'
# For direct access to the selected filenames
__datasource__ = __register__.getDataSourceViewer()

''' User Interface '''
# Output Folder
out_folder = Par('file')
out_folder.dtype = 'folder'
output_xyd = Par('bool','False')
output_xyd.title = "XYD"
output_cif = Par('bool','True')
output_cif.title = "CIF"
output_fxye = Par('bool','True')
output_fxye.title = "GSAS FXYE"
output_stem = Par('string','reduced')
output_stem.title = "Include in filename:"
Group('Output Format').add(output_xyd,output_cif,output_fxye,out_folder)
Group('Output Filename: ECH00NNNNN_+...').add(output_stem)
# Normalization
# We link the normalisation sources to actual dataset locations right here, right now
norm_table = {'Monitor 1':'bm1_counts','Monitor 2':'bm2_counts',
              'Monitor 3':'bm3_counts','Detector time':'detector_time'}
norm_apply     = Par('bool', 'True')
norm_apply.title = 'Apply'
norm_reference = Par('string', 'Monitor 3', options = norm_table.keys())
norm_reference.title = 'Source'
norm_target    = 'auto'
norm_plot = Act('plot_norm_proc()','Plot')
Group('Normalization').add(norm_apply, norm_reference,norm_plot)

# Background Correction
bkg_apply = Par('bool', 'False')
bkg_apply.title = 'Apply'
bkg_map   = Par('file', '')
bkg_map.title = 'Bkg File'
bkg_map.ext = '*.hdf'
bkg_show  = Act('bkg_show_proc()', 'Show') 
Group('Background Correction').add(bkg_apply, bkg_map, bkg_show)

# Vertical Tube Correction
vtc_apply = Par('bool', 'True')
vtc_apply.title = 'Apply'
vtc_file  = Par('file', '')
vtc_file.title = 'VTC file'
vtc_file.ext = '*.txt,*.*'
vtc_show  = Act('vtc_show_proc()', 'Show') 
Group('Vertical Tube Correction').add(vtc_apply, vtc_file, vtc_show)

# Efficiency Correction
eff_apply = Par('bool', 'True')
eff_apply.title = 'Apply'
eff_map   = Par('file', '')
eff_map.title = 'Efficiency File'
eff_map.ext = '*.*'
eff_show  = Act('eff_show_proc()', 'Show') 
Group('Efficiency Correction').add(eff_apply, eff_map, eff_show)

# Horizontal Tube Correction
htc_apply = Par('bool', 'True')
htc_apply.title = 'Apply'
htc_file  = Par('file', '')
htc_file.title = 'HTC file'
htc_file.ext = '*.ang,*.*'
htc_show  = Act('htc_show_proc()', 'Show') 
Group('Horizontal Tube Correction').add(htc_apply, htc_file, htc_show)

# Assemble (note this is before rescaling)
asm_drop_frames = Par('string')
asm_drop_frames.title = 'Remove frames:'
Group('Assemble frames').add(asm_drop_frames)

# Vertical Integration (note that gain recalc will include vertical integration)
vig_lower_boundary = Par('int', '0')
vig_lower_boundary.title = 'Lower limit'
vig_upper_boundary = Par('int', '127')
vig_upper_boundary.title = 'Upper limit'
vig_apply_rescale  = Par('bool', 'False')
vig_apply_rescale.title = 'Rescale'
vig_rescale_target = Par('float', '10000.0')
vig_rescale_target.title = 'Rescale target:'
vig_cluster = Par('bool',True)
vig_cluster.title = 'Merge close points'
Group('Vertical Integration').add(vig_lower_boundary, vig_upper_boundary, vig_cluster, vig_apply_rescale, vig_rescale_target)

# Recalculate gain
regain_apply = Par('bool','False')
regain_apply.title = 'Apply'
regain_iterno = Par('int','5')
regain_iterno.title = 'Iterations'
Group('Recalculate Gain').add(regain_apply,regain_iterno)

# Plot Helper: always Plot2 to Plot 3
plh_copy = Act('plh_copy_proc()', 'Copy plot')
Group('Copy 1D Datasets to Plot 3').add(plh_copy)

# Allow summation of plots
plh_sum = Act('plh_sum_proc()','Sum datasets')
plh_sum_type = Par('string','Ideal',options=['Ideal','Cluster','Merge Only'])
plh_cluster = Par('string','0.03')
plh_file = Par('file','')
Group('Sum 1D datasets in Plot 3').add(plh_file,plh_sum_type,plh_cluster,plh_sum)

# Delete plots
plh_dataset = Par('string', 'All', options = ['All'])
plh_delete  = Act('plh_delete_proc()', 'Delete')
Group('Delete 1D Datasets').add(plh_dataset, plh_delete)

#Preferences
pref_act = Act('save_user_prefs()','Save Defaults')
Group('Preferences').add(pref_act)

# Storage for efficiency map
if not 'eff_map_cache' in globals():
    eff_map_cache = {}
    
''' Button Actions '''

def show_helper(filename, plot, pre_title = ''):
    if filename:
        
        ds = Dataset(str(filename))
        
        if ds.ndim == 4:
            plot.set_dataset(ds[0, 0])
            plot.title = ds.title + " (first frame)"
        elif ds.ndim == 3:
            plot.set_dataset(ds[0])
            plot.title = ds.title + " (first frame)"
        else:
            plot.set_dataset(ds)
        
        if pre_title:
            plot.title = pre_title + plot.title
            
    else:
        print 'no valid filename was specified'
            
# Plot normalisation info
def plot_norm_proc():
    norm_source = norm_table[str(norm_reference.value)]
    dss = __datasource__.getSelectedDatasets()
    Plot2.clear()
    for fn in dss:
        loc = fn.getLocation()
        dset = df[str(loc)]
        plot_data = Dataset(getattr(dset,norm_source))
        plot_data = plot_data/plot_data.max()
        plot_data.title = os.path.basename(str(loc))+':' + str(norm_reference.value)
        Plot2.add_dataset(plot_data)

# show Background Correction Map
def bkg_show_proc():
    show_helper(bkg_map.value, Plot1, "Background Map: ")

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

# For HDF files
# show_helper(eff_map.value, Plot1, "Efficiency Map: ")

# show Vertical Tube Correction
def vtc_show_proc():
    if vtc_file.value:
        f = None
        try:
            # open file
            f  = open(str(vtc_file.value), 'r')
            ds = zeros(128, int)
            
            # read file
            for line in f:
                if type(line) is str:
                    line = line.strip()
                    if (len(line) > 0) and not line.startswith('#'):
                        items = line.split()
                        if len(items) == 2:
                            x_index  = int(items[0]) - 1 # from [1..128] to [0..127]
                            offset   = int(items[1])
                            
                            ds[x_index]     = offset
                            ds.var[x_index] = 0
                            
            # show result
            ds.title = 'Vertical Tube Correction'
            
            # show plot
            Plot3.set_dataset(ds)

        finally:
            if f != None:
                f.close()
    else:
        print 'no valid filename was specified'
# show Horizontal Tube Correction
def htc_show_proc():
    global Plot3
    if htc_file.value:
        f = None
        try:
            # open file
            f  = open(str(htc_file.value), 'r')
            ds = zeros(128)
            
            # read file
            index = 0
            for line in f:
                if type(line) is str:
                    line = line.strip()
                    if (len(line) > 0) and not line.startswith('#'):
                        ds[index]     = float(line)
                        ds.var[index] = 0
                        index         += 1
                            
            # show result
            ds.title = 'Horizontal Tube Correction'
            
            # show plot
            Plot3.set_dataset(ds)

        finally:
            if f != None:
                f.close()
    else:
        print 'no valid filename was specified'

def plh_copy_proc():
    # We copy from Plot 2 to Plot 3 only
    print 'Test printing from button actions'
    src = 'Plot 2'
    dst = 'Plot 3'
    
    plots = {'Plot 1': Plot1, 'Plot 2': Plot2, 'Plot 3': Plot3}

    src_plot = plots[src]
    dst_plot = plots[dst]
    
    src_ds = src_plot.ds
    if type(src_ds) is not list:
        print 'source plot does not contain 1D datasets'
        return
    
    dst_ds = dst_plot.ds
    if type(dst_ds) is not list:
        dst_ds = []
    
    dst_ds_ids = [id(ds) for ds in dst_ds]
    
    for ds in src_ds:
        if id(ds) not in dst_ds_ids:
            dst_plot.add_dataset(ds)

    # Update the options for deleting datasets
    target_list = ['All']
    for ds in src_plot.ds:
        target_list.append(ds.title)
    plh_dataset.options = target_list
    plh_dataset.value   = 'All'

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
    # Plot 3 hard-coded for simplicity
    target  = 'Plot 3'
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
        plh_dataset.options = []
    else:
        for ds in target_ds:
            if ds.title == dataset:
                target_plot.remove_dataset(ds)
        target_list = ['All']
        for ds in target_plot.ds:
            target_list.append(ds.title)
        plh_dataset.options = target_list
        plh_dataset.value   = 'All'

def plh_sum_proc():
    """Sum all datasets contained in plot 3"""
    datasets = Plot3.ds
    approach = str(plh_sum_type.value)
    if approach == 'Ideal':
        newds = reduction.sum_datasets(datasets)
        Plot2.set_dataset(newds)
    else:
        fs = reduction.merge_datasets(datasets)
        if approach == 'Cluster':
            cluster = float(plh_cluster.value)
            fs = reduction.debunch(fs,cluster)
        Plot2.set_dataset(fs)

# The preference system: 
def load_user_prefs():
    print 'In load user prefs'
    # Run through our parameters, looking for the corresponding
    # preferences
    p = globals().scope_keys()
    for name in p:
        if eval('isinstance('+ name + ',Par)'):
            execstring = name + '.value = "' + get_prof_value(name) + '"'
            exec execstring in globals()
            print 'Set %s to %s' % (name,str(eval(name+'.value')))

def save_user_prefs():
    print 'In save user prefs'
    # sneaky way to get all the preferences
    p = globals().scope_keys()
    for name in p:
        if eval('isinstance('+ name + ',Par)'):
            set_prof_value(name,str(eval(name + '.value')))
            print 'Set %s to %s' % (name,str(get_prof_value(name)))

''' Script Actions '''

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    
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
        norm_tar = str(norm_target).lower()

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
    
    # check if bkg-map needs to be loaded
    if bkg_apply.value:
        if not bkg_map.value:
            bkg = None
            print 'WARNING: no bkg-map was specified'
        else:
            bkg = Dataset(str(bkg_map.value))
    else:
        bkg = None
    
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
    # check if horizontal tube correction needs to be loaded
    if htc_apply.value:
        if not htc_file.value:
            htc = None
            print 'WARNING: no htc-file was specified'
        else:
            htc = str(htc_file.value)
    else:
        htc = None
        
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
        else:
            ds = rs
        if bkg:
            ds = reduction.getBackgroundCorrected(ds, bkg, norm_table[norm_ref], norm_tar)
        
        print 'Finished normalisation, background subtraction at %f' % (time.clock()-elapsed)
        # check if vertical tube correction is required
        if vtc:
            ds = reduction.getVerticallyCorrected(ds, vtc)
        print 'Finished vertical offset correction at %f' % (time.clock()-elapsed)
        # check if efficiency correction is required
        if eff:
            ds = reduction.getEfficiencyCorrected(ds, eff)
        
        print 'Finished efficiency correction at %f' % (time.clock()-elapsed)
        # Before fiddling with axes, get the ideal stepsize
        stepsize = reduction.get_stepsize(ds)
        print 'Ideal stepsize determined to be %f' % stepsize
        # check if horizontal tube correction is required
        if htc:
            ds = reduction.getHorizontallyCorrected(ds, htc)

        print 'Finished horizontal correction at %f' % (time.clock()-elapsed)

        # check if we are recalculating gain 
        if regain_apply.value:
           bottom = int(vig_lower_boundary.value)
           top = int(vig_upper_boundary.value)
           cs,gain,esds,chisquared = reduction.do_overlap(ds,regain_iterno.value,bottom=bottom,top=top)
           if cs is not None:
               print 'Have new gains at %f' % (time.clock() - elapsed)
               Plot4 = Plot(title='Chi squared history')
               Plot5 = Plot(title='Final Gain')
               fg = Dataset(gain)
               fg.var = esds
           # set horizontal axis (ideal values)
               Plot4.set_dataset(Dataset(chisquared))   #chisquared history
               Plot5.set_dataset(fg)   #final gain plot
           # assemble dataset, but if we have applied gain this is purely
           # for display purposes
        if ds.ndim > 2:
            ds = reduction.getStitched(ds)
        # Display dataset
        print 'Finished stitching at %f' % (time.clock()-elapsed)
        Plot1.set_dataset(ds)
        Plot1.title = ds.title
        if not vig_apply_rescale.value:
            norm_const = -1.0
        else:
            norm_const = float(vig_rescale_target.value)
        # set the cluster value
        if vig_cluster.value is True:
            cluster = stepsize * 0.6  #60 percent of ideal
        else:
            cluster = 0.0
        if not regain_apply.value or cs is None:  #already done
            cs = reduction.getVerticalIntegrated(ds, axis=0, normalization=norm_const,
                                                 cluster=cluster,bottom = int(vig_lower_boundary.value),
                                                 top=int(vig_upper_boundary.value))
            print 'Finished vertical integration at %f' % (time.clock()-elapsed)
        # Display reduced dataset
        Plot2.set_dataset(cs)
        Plot2.title = cs.title
        # Output datasets
        filename_base = join(str(out_folder.value),basename(str(fn))[:-7] + '_' + str(output_stem.value))
        if output_cif.value:
            output.write_cif_data(cs,filename_base)
        if output_xyd.value:
            output.write_xyd_data(cs,filename_base)
        if output_fxye.value:
            output.write_fxye_data(cs,filename_base)
        # ds.save_copy(join(str(out_folder.value), 'reduced_' + basename(str(fn))))
        print 'Finished writing data at %f' % (time.clock()-elapsed)
        
# dispose
def __dispose__():
    global Plot1,Plot2,Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()


''' Quick-Fix '''

def run_action(act):
    import sys
    act.set_running_status()
    try:
        exec(act.command)
        act.set_done_status()
    except:
        act.set_error_status()
        traceback.print_exc(file = sys.stdout)
        raise Exception, 'Error in running <' + act.text + '>'

''' Execute this each time it is loaded to reload user preferences '''

load_user_prefs()
