# Script control setup area
__script__.title     = 'ECH Reduction'
__script__.version   = '1.0'
# Add custom path
import sys

''' User Interface '''

# Output Folder
out_folder = Par('file')
out_folder.dtype = 'folder'
output_xyd = Par('bool','False')
output_cif = Par('bool','True')
output_fxye = Par('bool','True')
output_stem = Par('string','reduced_')
Group('Output Folder').add(output_xyd,output_cif,output_fxye,output_stem,out_folder)

# Normalization
# We link the normalisation sources to actual dataset locations right here, right now
norm_table = {'Monitor 1':'bm1_counts','Monitor 2':'bm2_counts',
              'Monitor 3':'bm3_counts','Detector time':'detector_time'}
norm_apply     = Par('bool', 'True')
norm_reference = Par('string', 'Monitor 3', options = norm_table.keys())
norm_target    = Par('string', 'auto')
Group('Normalization').add(norm_apply, norm_reference, norm_target)

# Background Correction
bkg_apply = Par('bool', 'False')
bkg_map   = Par('file', '')
bkg_map.ext = '*.hdf'
bkg_show  = Act('bkg_show_proc()', 'Show') 
Group('Background Correction').add(bkg_apply, bkg_map, bkg_show)

# Vertical Tube Correction
vtc_apply = Par('bool', 'True')
vtc_file  = Par('file', '')
vtc_file.ext = '*.txt,*.*'
vtc_show  = Act('vtc_show_proc()', 'Show') 
Group('Vertical Tube Correction').add(vtc_apply, vtc_file, vtc_show)

# Efficiency Correction
eff_apply = Par('bool', 'True')
eff_map   = Par('file', '')
eff_map.ext = '*.*'
eff_show  = Act('eff_show_proc()', 'Show') 
Group('Efficiency Correction').add(eff_apply, eff_map, eff_show)

# Horizontal Tube Correction
htc_apply = Par('bool', 'True')
htc_file  = Par('file', '')
htc_file.ext = '*.ang,*.*'
htc_show  = Act('htc_show_proc()', 'Show') 
Group('Horizontal Tube Correction').add(htc_apply, htc_file, htc_show)

# Recalculate gain
regain_apply = Par('bool','True')
regain_iterno = Par('int','5')
regain_exact_angles = Par('bool','False')  #use exact tube angles
regain_finish = Par('bool','True')         #use output of refinement as final data
Group('Recalculate Gain').add(regain_apply,regain_iterno)

# Assemble
asm_algorithm = Par('string', 'stitch frames', options = ['stitch frames', 'sum frames'])
Group('Assemble').add(asm_algorithm)

# Vertical Integration
vig_lower_boundary = Par('int', '0')
vig_upper_boundary = Par('int', '127')
vig_apply_rescale  = Par('bool', 'True')
vig_rescale_target = Par('float', '10000.0')
vig_cluster = Par('float','0.03')
Group('Vertical Integration').add(vig_lower_boundary, vig_upper_boundary, vig_cluster, vig_apply_rescale, vig_rescale_target)

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
            
# show Background Correction Map
def bkg_show_proc():
    show_helper(bkg_map.value, Plot1, "Background Map: ")

# show Efficiency Correction Map 
def eff_show_proc():
    from Reduction import reduction
    if not eff_map.value in eff_map_cache:
        eff_map_cache[eff_map.value] = reduction.read_efficiency_cif(eff_map.value)
    else:
        print 'Found in cache ' + `eff_map_cache[eff_map.value]`
    Plot1.set_dataset(eff_map_cache[eff_map.value][0])
    Plot1.title = 'Efficiency map'

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
            Plot1.set_dataset(ds)

        finally:
            if f != None:
                f.close()
    else:
        print 'no valid filename was specified'
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
            if not eff_map.value in eff_map_cache:
                eff_map_cache[eff_map.value] = reduction.read_efficiency_cif(str(eff_map.value))
            else:
                print 'Found cached efficiency map ' + str(eff_map.value)
            eff = eff_map_cache[eff_map.value]
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
        # check if horizontal tube correction is required
        if htc:
            ds = reduction.getHorizontallyCorrected(ds, htc)

        print 'Finished horizontal correction at %f' % (time.clock()-elapsed)

        # check if we are recalculating gain
        if regain_apply.value:
           print 'ds.has_key(ms): ' + `ds.__dict__.has_key('ms')`
           ds,gain,esds,chisquared = reduction.do_overlap(ds,regain_iterno.value)
           print 'Have new gains at %f' % (time.clock() - elapsed)
           Plot4 = Plot(title='Chi squared history')
           Plot5 = Plot(title='Final Gain')
           fg = Dataset(gain)
           fg.var = esds
           # set horizontal axis (ideal values)
           Plot4.set_dataset(Dataset(chisquared))   #chisquared history
           Plot5.set_dataset(fg)   #final gain plot
        if regain_finish.value is True:
            # not yet done - we take the output of the refinement as the final data
            pass
        # assemble dataset
        if ds.ndim > 2:
            asm_algo = str(asm_algorithm.value)
            if asm_algo == 'stitch frames':
                ds = reduction.getStitched(ds)
            elif asm_algo == 'sum frames':
                ds = reduction.getSummed(ds)
            else:
                print 'specify assemble algorithm'
                return
        # Display dataset
        print 'Finished stitching at %f' % (time.clock()-elapsed)
        Plot1.set_dataset(ds)
        Plot1.title = ds.title
        if vig_apply_rescale.value:
            ds = reduction.getVerticalIntegrated(ds, axis=0, normalization=float(vig_rescale_target.value),
                                                 cluster=float(vig_cluster.value))
        else:
            ds = reduction.getVerticalIntegrated(ds, axis=0, cluster=float(vig_cluster.value))
        print 'Finished vertical integration at %f' % (time.clock()-elapsed)
        # Display reduced dataset
        Plot2.set_dataset(ds)
        Plot2.title = ds.title
        # Output datasets
        filename_base = join(str(out_folder.value),str(output_stem.value) + basename(str(fn))[:-7])
        if output_cif.value:
            output.write_cif_data(ds,filename_base)
        if output_xyd.value:
            output.write_xyd_data(ds,filename_base)
        if output_fxye.value:
            output.write_fxye_data(ds,filename_base)
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
    act.set_running_status()
    try:
        exec(act.command)
        act.set_done_status()
    except:
        act.set_error_status()
        traceback.print_exc(file = sys.stdout)
        raise Exception, 'Error in running <' + act.text + '>'

