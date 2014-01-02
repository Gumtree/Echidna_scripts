# Script control setup area
__script__.title     = 'ECH Toolbox'
__script__.version   = '1.0'
__datasource__ = __register__.getDataSourceViewer()
from Reduction import reduction

''' User Interface '''
# Plot Helper: always Plot2 to Plot 3
# At the top for convenience
plh_copy = Act('plh_copy_proc()', 'Copy plot')
Group('Copy 1D Datasets to Plot 3').add(plh_copy)

# Show info
# What we show
info_table = {'Proposal Number':'experiment_title',
              'User':'user',
              'Sample Name': 'sample_name',
              'Mono': 'mom',
              'Setup': '/entry1/sample/description',
              'Start': 'stth',
              'Step count time':'detector_time',
              'Start time': '$entry/start_time'}
extra_info_table = {'TC1 setpoint':'/entry1/sample/tc1/sensor/setpoint1',
                    'TC2 setpoint':'/entry1/sample/tc1/sensor/setpoint2',
                    'TC3 setpoint':'/entry1/sample/tc2/sensor/setpoint1'}
full_info = Par('bool','False')
info_show = Act('info_show_proc()', 'Show File information')
Group('Information').add(full_info,info_show)
# The tuple for each key contains the location, axis label (for the plot), and
# the value of error for display as a percentage of the measured value. If a
# negative error is given, counting statistics are assumed
plot_choice_table = {'TC1':('/entry1/sample/tc1/sensor/sensorValueA','Temperature',2.0),
                     'TC2':('/entry1/sample/tc1/sensor/sensorValueB','Temperature',2.0),
                     'Magnet Stick 1':('/entry1/sample/tc1/Loop2/sensor','Temperature',2.0),
                     'Magnet Stick 2':('/entry1/sample/tc1/Loop2/sensor','Temperature',2.0),
                     'Magnet Heat Exchanger':('/entry1/sample/tc1/Loop1/sensor','Temperature',2.0),
                     'Total counts':('/entry1/data/total_counts','Counts',-1)}
neat_keys = plot_choice_table.keys()
neat_keys.sort()
plot_choice = Par('string','',options=neat_keys)
plot_choice.title = 'Item to plot'# The tuple for each key contains the location, axis label (for the plot), and
plot_info = Act('plot_values_proc()','Plot selected values')
Group('Plotting').add(plot_choice,plot_info)
# Re-prepare the GUI with current plot contents
prepare_act = Act('prepare_proc()','Prepare')
Group('Prepare').add(prepare_act)
# Some maths operations
first_ds = Par('string','',options=[])
subbed_ds = Par('string','',options=[])
subbed_plot_act = Act('sub_plot_proc()','Subtract')
Group('Subtraction').add(first_ds,subbed_ds,subbed_plot_act)
# Multiplication
mult_ds = Par('string','',options=[])
mult_fact = Par('string','1.0')
mult_act = Act('mult_proc()','Multiply')
Group('Multiplication').add(mult_ds,mult_fact,mult_act)
# Import external file
external_filename = Par('file','')
external_wavelength = Par('float',1.622)
import_act = Act('import_proc()','Import File')
Group('Import').add(external_filename,external_wavelength,import_act)
# Plot settings
ps_plotname = Par('string','Plot 2',options=['Plot 2','Plot 3'])
ps_dspacing = Par('bool',False,command='dspacing_change()')
Group('Plot settings').add(ps_plotname,ps_dspacing)


''' Button callbacks '''

def prepare_proc():
    """Load the plot titles into the GUI"""
    global Plot2,Plot3
    curves = []
    if Plot2.ds is not None:
        curves = curves + map(lambda a:a.title,Plot2.ds)
    if Plot3.ds is not None:
        curves = curves + map(lambda a:a.title,Plot3.ds)
    first_ds.options = curves
    subbed_ds.options = curves
    mult_ds.options = curves

def sub_plot_proc():
    """Subtract two datasets given their titles only"""
    # We use the same approach as summation in the
    # main Echidna GUI routines. We first merge,
    # then sum.
    top_name = str(first_ds.value)
    bot_name = str(subbed_ds.value)
    top_ds,t = find_ds_by_title(top_name)
    bottom_ds,b = find_ds_by_title(bot_name)
    neg_ds = bottom_ds * (-1.0)
    final_ds = reduction.merge_datasets([top_ds,neg_ds])
    final_ds = reduction.debunch(final_ds,0.03)  #for testing, for now
    final_ds.title = 'Subtracted datasets'
    Plot2.set_dataset(final_ds)

def mult_proc():
    """Multiply a dataset given the title"""
    global Plot2,Plot3
    mult_name = str(mult_ds.value)
    target_ds,target_plot = find_ds_by_title(mult_name)
    final_ds = target_ds * float(mult_fact.value)
    target_plot.remove_dataset(target_ds)
    target_plot.add_dataset(final_ds)

def find_ds_by_title(title):
    """Utility function to find a dataset in a plot by title"""
    global Plot2,Plot3
    for one_plot in [Plot2,Plot3]:
        dss = one_plot.ds
        if dss is None:
            continue
        titles = map(lambda a:a.title,dss)
        if titles.count(title) == 1:
           return dss[titles.index(title)], one_plot
        elif titles.count(title)>1:
           print 'Error: ambiguous title %s' % title

def info_show_proc():
    import os,datetime
    dss = __datasource__.getSelectedDatasets()
    for fn in dss:
        loc = fn.getLocation()
        dset = df[str(loc)]
        filename = os.path.basename(str(loc))
        print '\nInformation for filename: %s\n' % filename
        final_table = info_table
        if full_info.value:
            final_table.update(extra_info_table)
        for key in final_table:
            true_key = final_table[key]
            try:
                value = getattr(dset,true_key)
            except:
                try:
                    value = SimpleData(dset.__iNXroot__.findContainerByPath(true_key))
                except:
                    continue
            if len(value) > 1 and value.dtype != type(''):
                value = value[0]
            print '%20s:  %s' % (key,value)
        # Now for the other values
        print '%20s:  %s' % ('Number of steps',len(dset['stth']))
        start_time = datetime.datetime.strptime(str(dset['$entry/start_time']),"%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(str(dset['$entry/end_time']),"%Y-%m-%d %H:%M:%S")
        print '%20s:  %s' % ('Total time',"%s" % (end_time-start_time))

def plot_values_proc():
    """Plot the selected values to Plot 2"""
    import os
    dss = __datasource__.getSelectedDatasets()
    target = str(plot_choice.value)
    for fn in dss:
        loc = fn.getLocation()
        dset = df[str(loc)]
        filename = os.path.basename(str(loc))
        print '\nInformation for filename: %s\n' % filename
        try:
            true_key = plot_choice_table[target][0]
        except KeyError: # user input directly
            true_key = target
        try:
            value = getattr(dset,true_key)
        except:
            try:
               value = SimpleData(dset.__iNXroot__.findContainerByPath(true_key))
            except:
               continue
        # Print raw values
        print "%s: " % target + `value`
        dset = Dataset(value)
        # figure out variance
        try:
            error_calc = plot_choice_table[target][2]
        except KeyError:
            error_calc = 2.0
        if error_calc < 0:
            dset.var = dset.storage
        else:   
            dset.var = (dset.storage * error_calc / 100.0)**2
        dset.title = filename + ":" + target
        Plot2.set_dataset(dset)
        Plot2.x_label = 'Step'
        Plot2.title = 'Information plot'
        try:
            Plot2.y_label = plot_choice_table[target][1]
        except KeyError:
            Plot2.y_label = target

def import_proc():
    """Import a three-column ASCII file (TODO: CIF). Any line whose first non-whitespace character
    is not [0-9.+-] is considered to be a comment and ignored. Columns are assumed to be in
    order of angle,intensity,error."""
    from Reduction import AddCifMetadata
    import_file = str(external_filename.value)
    import_wl = float(external_wavelength.value)
    lines = open(import_file).readlines()
    print 'File %s: %d lines read in' % (import_file,len(lines))
    # Remove empty lines
    lines = map(lambda a:a.strip(),lines)
    lines = filter(lambda a:len(a)>0,lines)
    # Choose only numeric-valued lines
    lines = filter(lambda a:a.strip()[0] in '0123456789.+-',lines)
    print 'File %s: %d lines accepted' % (import_file,len(lines))
    split_lines = map(lambda a:a.split(),lines)
    float_lines = map(lambda b:map(lambda a:float(a),b),split_lines)
    columns = zip(*float_lines)
    # Now create the dataset
    ds = Dataset(columns[1])
    # Auto-detect GSAS centidegrees
    axis = Array(columns[0])
    if axis.max() > 361:
        # Assume centidegrees
        axis = axis/100.0
    ds.set_axes([axis],anames=['Two theta'],aunits=['Degrees'])
    if len(columns)>=3:
        ds.var = Array(columns[2])**2
    AddCifMetadata.add_metadata_methods(ds)
    ds.add_metadata("_diffrn_radiation_wavelength",import_wl,"CIF")
    ds.title = os.path.basename(import_file)
    Plot2.set_dataset(ds)
    Plot2.title = ds.title
    
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
            send_to_plot(ds,dst_plot,add=True,add_timestamp=False)

def dspacing_change():
    """Toggle the display of d spacing on the horizontal axis"""
    global Plot2,Plot3
    from Reduction import reduction
    plot_table = {'Plot 2':Plot2, 'Plot 3':Plot3}
    target_plot = plot_table[str(ps_plotname.value)]
    if target_plot.ds is None:
        return
    # Preliminary check we are not displaying something
    # irrelevant, e.g. monitor counts
    for ds in target_plot.ds:
        if ds.axes[0].name not in ['Two theta','d-spacing']:
            return
    change_dss = copy(target_plot.ds)
    # Check to see what change is required
    need_d_spacing = ps_dspacing.value
    # target_plot.clear() causes problems; use 'remove' instead
    # need to set the xlabel by hand due to gplot bug
    if need_d_spacing: target_plot.x_label = 'd-spacing (Angstroms)'
    elif not need_d_spacing: target_plot.x_label = 'Two theta (Degrees)'
    target_plot.y_label = 'Intensity'
    for ds in change_dss:
        current_axis = ds.axes[0].name
        print '%s has axis %s' % (ds.title,current_axis)
        if need_d_spacing:    
            result = reduction.convert_to_dspacing(ds)
        elif not need_d_spacing:
            result = reduction.convert_to_twotheta(ds)
        if result == 'Changed':
            target_plot.remove_dataset(ds)
            target_plot.add_dataset(ds)
