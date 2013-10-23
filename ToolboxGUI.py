# Script control setup area
__script__.title     = 'ECH Toolbox'
__script__.version   = '1.0'
__datasource__ = __register__.getDataSourceViewer()

''' User Interface '''

# Show info
# What we show
info_table = {'Proposal Number':'experiment_title',
              'User':'user',
              'Sample Name': 'sample_name',
              'Mono': 'mom',
              'Setup': '/entry1/sample/description'}
full_info = Par('bool','False')
info_show = Act('info_show_proc()', 'Show File information')
Group('Information').add(full_info,info_show)

''' Button callbacks '''

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
        
