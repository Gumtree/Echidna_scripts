# Script control setup area
script_source = '/home/jrh/programs/echidna/Gumtree_scripts'
__script__.title     = 'ECH Calibration'
__script__.version   = '1.0'
__script__.dict_path = script_source + '/ECH/path_table'
# Add custom path
import sys
if script_source not in sys.path:
    sys.path = [script_source] + sys.path

''' User Interface '''

from datetime import date
today = date.today()

# Input
in_van_run  = Par('file', '')
in_van_run.ext = '*.hdf'
in_van_show = Act('in_van_show_proc()', 'Show') 
in_bkg_run  = Par('file', '')
in_bkg_run.ext = '*.hdf'
in_bkg_show = Act('in_bkg_show_proc()', 'Show')
Group('Input').add(in_van_run, in_van_show, in_bkg_run, in_bkg_show)

# Output Folder
out_folder = Par('file', script_source + '/Data/')
out_folder.dtype = 'folder'
Group('Output Folder').add(out_folder)

# Normalization
norm_apply     = Par('bool'  , 'True'      )
norm_reference = Par('string', 'bm1 counts', options = ['bm1 counts', 'bm2 counts', 'bm3 counts', 'detector time'])
Group('Normalization').add(norm_apply, norm_reference)

## Background Correction Map
#bkg_make = Par('bool'  , 'True')
#bkg_name = Par('string', today.strftime("bkg_%Y_%m_%d.hdf"))
#Group('Background Correction Map').add(bkg_make, bkg_name)

# Efficiency Correction Map
eff_make = Par('bool'  , 'True')
eff_name = Par('string', today.strftime("eff_%Y_%m_%d.hdf"))
eff_std_range      = Par('float' , '1.8' )
eff_lower_boundary = Par('int'   , '0'   )
eff_upper_boundary = Par('int'   , '127' )
Group('Efficiency Correction Map').add(eff_make, eff_name, eff_std_range, eff_lower_boundary, eff_upper_boundary)

# Vertical Tube Correction List
vtc_make      = Par('bool'  , 'True')
vtc_name      = Par('string', today.strftime("vertical_offsets_%Y_%m_%d.txt"))
vtc_algorithm = Par('string', 'Vertically Centered Average', options = ['Vertically Centered Average'])
Group('Vertical Tube Correction List').add(vtc_make, vtc_algorithm, vtc_name)


''' Load Preferences '''

calibration_output_dir  = __UI__.getPreference("au.gov.ansto.bragg.echidna.ui:calibration_output_dir")
normalisation_reference = __UI__.getPreference("au.gov.ansto.bragg.echidna.ui:normalisation_reference")

if calibration_output_dir:
    out_folder.value = calibration_output_dir
if normalisation_reference:
    if normalisation_reference == 'bm1_counts':
        norm_reference.value = 'bm1 counts'
    elif normalisation_reference == 'bm2_counts':
        norm_reference.value = 'bm2 counts'
    elif normalisation_reference == 'bm3_counts':
        norm_reference.value = 'bm3 counts'
    elif normalisation_reference == 'detector_counts':
        norm_reference.value = 'detector counts'


''' Button Actions '''
        
def show_helper(filename, plot, pre_title = ''):
    if filename:
        
        ds = Dataset(str(filename))
        plot.clear()
        
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

# show input Vanadium Map
def in_van_show_proc():
    show_helper(in_van_run.value, Plot1, "Vanadium Map: ")

# show input Background Map
def in_bkg_show_proc():
    global Plot2
    show_helper(in_bkg_run.value, Plot2, "Background Map: ")

def get_norm_ref(ds, ref_name):
    if ref_name == 'bm1 counts':
        return ds.bm1_counts
    elif ref_name == 'bm2 counts':
        return ds.bm2_counts
    elif ref_name == 'bm3 counts':
        return ds.bm3_counts
    elif ref_name == 'detector time':
        return ds.detector_time
    else:
        raise Exception('specify normalization reference')

''' Script Actions '''

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    
    from Reduction import reduction
    from os.path import join
    
    df.datasets.clear()
    
    # check input
    if not in_van_run.value:
        print 'specify vanadium run'
        return
    if not in_bkg_run.value:
        print 'specify background run'
        return
    
    van = Dataset(str(in_van_run.value))
    bkg = Dataset(str(in_bkg_run.value))
    
    # check if input is correct
    if van.ndim != 4:
        raise AttributeError('van.ndim != 4')
    if bkg.ndim != 4:
        raise AttributeError('van.ndim != 4')
    if van.axes[0].title != 'azimuthal_angle':
        raise AttributeError('van.axes[0].title != azimuthal_angle')
    if bkg.axes[0].title != 'azimuthal_angle':
        raise AttributeError('bkg.axes[0].title != azimuthal_angle')
    if van.shape != bkg.shape: # checks number of frames and detector pixel dimensions
        raise AttributeError('van.shape != bkg.shape')

    # check if input needs to be normalized
    if norm_apply.value:
        norm_ref = str(norm_reference.value)
        
        ref_van = get_norm_ref(van, norm_ref)
        ref_bkg = get_norm_ref(bkg, norm_ref)
        
        # use maximal value of vanadium for reference
        norm_tar = max(ref_van)
        
        reduction.applyNormalization(van, reference=ref_van, target=norm_tar)
        reduction.applyNormalization(bkg, reference=ref_bkg, target=norm_tar)
    
    # sum input (float copies are not required, eff will be float anyway)
    # background correction is done in getEfficiencyCorrectionMap
    # (it does not matter if we subtract each bkg-frame from each van-frame and then sum the result or
    #  if we subtract the summed bkg-frames from the summed van-frames)
    van_sum = reduction.getSummed(van, floatCopy=False, applyStth=False)
    bkg_sum = reduction.getSummed(bkg, floatCopy=False, applyStth=False)
    
    if eff_make.value:
        # load ok map
        ok_map = reduction.getOkMap(                     \
            van_sum,                                     \
            stdRange=float(eff_std_range.value),         \
            lowerBoundary=int(eff_lower_boundary.value), \
            upperBoundary=int(eff_upper_boundary.value))
        eff = reduction.getEfficiencyCorrectionMap(van_sum, bkg_sum, ok_map)
        eff.save_copy(join(str(out_folder.value), str(eff_name.value)))

        reduction.getVerticalIntegrated(eff)
        
    # check if vertical tube correction list needs to be created
    if vtc_make.value:
        reduction.getVerticalCorrectionList(                                    \
            van_sum,                                                            \
            algorithm=str(vtc_algorithm.value),                                 \
            output_filename=join(str(out_folder.value), str(vtc_name.value)))

# dispose
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    
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
