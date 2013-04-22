import inspect
from java.lang import System
import time
import math
from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING
from gumpy.commons import sics
from Internal import sicsext
# Script control setup area
# script info
__script__.title = 'Device Alignment'
__script__.version = ''
#pact = Act('previous_step()', '<- Previous Step')
    
G1 = Group('Scan on device')
device_name = Par('string', 'dummy_motor', options = ['dummy_motor'], command = 'update_axis_name()')
scan_start = Par('float', 0)
scan_stop = Par('float', 0)
number_of_points = Par('int', 0)
scan_mode = Par('string', 'time')
scan_mode.enabled = True
scan_preset = Par('int', 0)
act1 = Act('scan_device()', 'Scan on Device')
def scan_device():
    aname = device_name.value
    try:
        if DEBUGGING :
            aname = 'dummy_motor'
    except:
        pass
    axis_name.value = aname
    slog('runscan ' + str(device_name.value) + ' ' + str(scan_start.value) + ' ' + str(scan_stop.value) \
                    + ' ' + str(number_of_points.value) + ' ' + str(scan_mode.value) + ' ' + str(scan_preset.value))
    sicsext.runscan(device_name.value, scan_start.value, scan_stop.value, number_of_points.value, 
                    scan_mode.value, scan_preset.value, load_experiment_data, True, \
                    'HISTOGRAM_XY')
    time.sleep(2)
    peak_pos.value = float('NaN')
    FWHM.value = float('NaN')
    fit_curve()
devices = sicsext.getDrivables()
device_name.options = devices
def update_axis_name():
    axis_name.value = device_name.value
        
G1.add(device_name, scan_start, scan_stop, number_of_points, scan_mode, scan_preset, act1)

G2 = Group('Fitting')
data_name = Par('string', 'bm2_counts', \
               options = ['total_counts', 'bm1_counts', 'bm2_counts'])
normalise = Par('bool', True)
axis_name = Par('string', '')
axis_name.enabled = True
fit_min = Par('float', 'NaN')
fit_max = Par('float', 'NaN')
peak_pos = Par('float', 'NaN')
FWHM = Par('float', 'NaN')
fact = Act('fit_curve()', 'Fit Again')
#offset_done = Par('bool', False)
#act3 = Act('offset_s2()', 'Set Device Zero Offset')
G2.add(data_name, normalise, axis_name, fit_min, fit_max, peak_pos, FWHM, fact)

def scan(dname, start, stop, np, mode, preset):
    device_name.value = dname
    scan_start.value = start
    scan_stop.value = stop
    number_of_points.value = np
    scan_mode.value = mode
    scan_preset.value = preset
    axis_name.value = dname
    scan_device()
    
#def fit_curve():
#    __std_fit_curve__()

def fit_curve():
    global Plot1
    ds = Plot1.ds
    if len(ds) == 0:
        log('Error: no curve to fit in Plot1.\n')
        return
    for d in ds:
        if d.title == 'fitting':
            Plot1.remove_dataset(d)
    d0 = ds[0]
    fitting = Fitting(GAUSSIAN_FITTING)
    try:
        fitting.set_histogram(d0, fit_min.value, fit_max.value)
        val = peak_pos.value
        if val == val:
            fitting.set_param('mean', val)
        val = FWHM.value
        if val == val:
            fitting.set_param('sigma', math.fabs(val / 2.35482))
        res = fitting.fit()
        res.var[:] = 0
        res.title = 'fitting'
        Plot1.add_dataset(res)
        mean = fitting.params['mean']
        mean_err = fitting.errors['mean']
        FWHM.value = 2.35482 * math.fabs(fitting.params['sigma'])
        FWHM_err = 5.54518 * math.fabs(fitting.errors['sigma'])
        log('POS_OF_PEAK=' + str(mean) + ' +/- ' + str(mean_err))
        log('FWHM=' + str(FWHM.value) + ' +/- ' + str(FWHM_err))
        log('Chi2 = ' + str(fitting.fitter.getQuality()))
        peak_pos.value = fitting.mean
#        print fitting.params
    except:
#        traceback.print_exc(file = sys.stdout)
        log('can not fit\n')


# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
#    __std_run_script__(fns)
    __std_run_script__(fns)

def load_experiment_data():
    basename = sicsext.getBaseFilename()
    fullname = str(System.getProperty('sics.data.path') + '/' + basename)
    df.datasets.clear()
    ds = df[fullname]
    dname = str(data_name.value)
    data = SimpleData(ds[dname])
#    data = ds[str(data_name.value)]
    axis = SimpleData(ds[str(axis_name.value)])
    if data.size > axis.size:
        data = data[:axis.size]
    if normalise.value :
        if dname == 'bm1_counts':
            tname = 'bm1_time'
        elif dname == 'bm2_counts':
            tname = 'bm2_time'
        else:
            tname = 'detector_time'
        norm = ds[tname]
        if norm != None and hasattr(norm, '__len__'):
            avg = norm.sum() / len(norm)
            niter = norm.item_iter()
            if niter.next() <= 0:
                niter.set_curr(1)
            data = data / norm * avg

    ds2 = Dataset(data, axes=[axis])
    ds2.title = ds.id
    ds2.location = fullname
    fit_min.value = axis.min()
    fit_max.value = axis.max()
    Plot1.set_dataset(ds2)
    Plot1.x_label = axis_name.value
    Plot1.y_label = str(data_name.value)
    Plot1.title = str(data_name.value) + ' vs ' + axis_name.value
    Plot1.pv.getPlot().setMarkerEnabled(True)

def __dataset_added__(fns = None):
    pass
    
def __std_run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
            ds = Plot1.ds
#            if ds != None and len(ds) > 0:
#                if ds[0].location == fn:
#                    return
            df.datasets.clear()
            ds = df[fn]
            axis_name.value = ds.axes[0].name
            dname = str(data_name.value)
            if dname == 'total_counts':
#                data = ds.sum(0)
                data = ds[dname]
            else:
                data = ds[dname]
            if normalise.value :
                if dname == 'bm1_counts':
                    tname = 'bm1_time'
                elif dname == 'bm2_counts':
                    tname = 'bm2_time'
                else:
                    tname = 'detector_time'
                norm = ds[tname]
                if norm != None and hasattr(norm, '__len__'):
                    avg = norm.sum() / len(norm)
                    niter = norm.item_iter()
                    if niter.next() <= 0:
                        niter.set_curr(1)
                    data = data / norm * avg
        
            axis = ds[str(axis_name.value)]
            ds2 = Dataset(data, axes=[axis])
            ds2.title = ds.id
            ds2.location = fn
            fit_min.value = axis.min()
            fit_max.value = axis.max()
            Plot1.set_dataset(ds2)
            Plot1.x_label = axis_name.value
            Plot1.y_label = dname
            Plot1.title = dname + ' vs ' + axis_name.value
            Plot1.pv.getPlot().setMarkerEnabled(True)
            peak_pos.value = float('NaN')
            FWHM.value = float('NaN')
            fit_curve()
            
def auto_run():
    pass

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
