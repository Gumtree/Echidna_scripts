__script__.title     = 'Plot monitor'
__script__.version   = '1.0'
#
#  Create the GUI
#
monitors = {'Pre-mono':'/entry1/monitor/bm1_counts',
            'Post-mono':'/entry1/monitor/bm2_counts',
            'Post-sample':'/entry1/monitor/bm3_counts'}
mon_choice = Par('string','Pre-mono',options=monitors.keys())
mon_choice.title = 'Location'
mon_norm = Par('bool','False')
mon_norm.title = 'Normalise'
Group('Monitor Plot').add(mon_choice,mon_norm)

def __run_script__(fns):
    # check input
    if (fns is None or len(fns) == 0) :  #user forgot to select
        print 'no input datasets'
        open_error('No input datasets')  #throw up an error box
        return                           #and we're done

    df.datasets.clear()                  #Erase previous fiddling
    clear_plot(Plot1)                    #Remove old plots
    mon_path = monitors[mon_choice.value]#Get the NeXuS path
    Plot1.set_x_label('Step')            #Configure the plot
    Plot1.set_title('Monitor counts')    #configure the plot
    for fn in fns:                       #Loop over all selected datasets
        ds = df[fn]                      #Create dataset from filename
        mon_counts = Dataset(ds[mon_path]) #Extract monitor counts
        if mon_norm.value is True:       #Are we normalising?
            real_mon_counts = mon_counts/mon_counts.max() #Normalise
            y_label = 'Normalised counts'
        else:                            #No normalisation
            real_mon_counts = mon_counts
            y_label = 'Counts'
        #Create informative legend
        real_mon_counts.title = ds['/entry1/sample/name'] + ':' + mon_choice.value
        Plot1.add_dataset(real_mon_counts)
        Plot1.set_y_label(y_label)       #Set custom y label
             
def clear_plot(plotname):
    all_datasets = copy(plotname.ds)
    if plotname.ds is None:
        return
    for ds in all_datasets:
        plotname.remove_dataset(ds)

