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
        
