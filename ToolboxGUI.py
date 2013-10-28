# Script control setup area
__script__.title     = 'ECH Toolbox'
__script__.version   = '1.0'
__datasource__ = __register__.getDataSourceViewer()
from Reduction import reduction

''' User Interface '''

# Show info
# What we show
info_table = {'Proposal Number':'experiment_title',
              'User':'user',
              'Sample Name': 'sample_name',
              'Mono': 'mom',
              'Setup': '/entry1/sample/description',
              'Start': 'stth',
              'Count time':'detector_time'}
full_info = Par('bool','False')
info_show = Act('info_show_proc()', 'Show File information')
Group('Information').add(full_info,info_show)
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
    import os
    dss = __datasource__.getSelectedDatasets()
    for fn in dss:
        loc = fn.getLocation()
        dset = df[str(loc)]
        filename = os.path.basename(str(loc))
        print '\nInformation for filename: %s\n' % filename
        for key in info_table:
            true_key = info_table[key]
            try:
                value = getattr(dset,true_key)
            except:
                try:
                    value = SimpleData(dset.__iNXroot__.findContainerByPath(true_key))
                except:
                    next
            if len(value) > 1 and value.dtype != type(''):
                value = value[0]
            print '%20s:  %s' % (key,value)
        
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
    
