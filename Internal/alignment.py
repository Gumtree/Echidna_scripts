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
__cur_scan_filename__ = None
#pact = Act('previous_step()', '<- Previous Step')
    
G1 = Group('Scan on device')
device_name = Par('string', 'dummy_motor', options = ['dummy_motor'], command = 'update_axis_name()')
scan_start = Par('float', 0)
scan_stop = Par('float', 0)
number_of_points = Par('int', 0)
scan_mode = Par('string', 'time')
scan_mode.enabled = False
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
                    scan_mode.value, scan_preset.value, load_experiment_data, True)
#    exec('sicsext.runscan(\'' + aname + '\', ' + scan.value + ', 0, \'call_back()\')')
    time.sleep(2)
    fit_curve()
devices = sicsext.getDrivables()
device_name.options = devices
def update_axis_name():
    axis_name.value = device_name.value
        
G1.add(device_name, scan_start, scan_stop, number_of_points, scan_mode, scan_preset, act1)

G2 = Group('Fitting')
data_name = Par('string', 'total_counts', \
               options = ['total_counts', 'bm1_counts', 'bm2_counts'])
axis_name = Par('string', '')
peak_pos = Par('float', 'NaN')
fact = Act('fit_curve()', 'Fit Again')
#offset_done = Par('bool', False)
#act3 = Act('offset_s2()', 'Set Device Zero Offset')
G2.add(data_name, axis_name, peak_pos, fact)

def scan(dname, start, stop, np, mode, preset):
    device_name.value = dname
    scan_start.value = start
    scan_stop.value = stop
    number_of_points.value = np
    scan_mode.value = mode
    scan_preset.value = preset
    axis_name = dname
    scan_device()
    
def fit_curve():
    __std_fit_curve__()

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
#    __std_run_script__(fns)
    __std_run_script__(fns)

def load_experiment_data():
    global __cur_scan_filename__
    basename = sicsext.getBaseFilename()
    fullname = str(System.getProperty('sics.data.path') + '/' + basename)
    df.datasets.clear()
    __cur_scan_filename__ = fullname
    ds = df[fullname]
    dname = str(data_name.value)
    data = SimpleData(ds[dname])
#    data = ds[str(data_name.value)]
    axis = SimpleData(ds[str(axis_name.value)])
    if data.size > axis.size:
        data = data[:axis.size]
    ds2 = Dataset(data, axes=[axis])
    ds2.title = ds.id
    ds2.location = fullname
    Plot1.set_dataset(ds2)
    Plot1.x_label = axis_name.value
    Plot1.y_label = str(data_name.value)
    Plot1.title = str(data_name.value) + ' vs ' + axis_name.value
    Plot1.pv.getPlot().setMarkerEnabled(True)

def __std_run_script__(fns):
    # Use the provided resources, please don't remove.
    global Plot1
    global Plot2
    global Plot3
    global __cur_scan_filename__
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
            if fn == __cur_scan_filename__:
                continue
            else :
                __cur_scan_filename__ = None
            ds = Plot1.ds
            if ds != None and len(ds) > 0:
                if ds[0].location == fn:
                    return
            df.datasets.clear()
            ds = df[fn]
            dname = str(data_name.value)
            if dname == 'total_counts':
#                data = ds.sum(0)
                data = ds[dname]
            else:
                data = ds[dname]
            qm = ds[str(axis_name.value)]
            ds2 = Dataset(data, axes=[qm])
            ds2.title = ds.id
            ds2.location = fn
            Plot1.set_dataset(ds2)
            Plot1.x_label = axis_name.value
            Plot1.y_label = dname
            Plot1.title = dname + ' vs ' + axis_name.value
            Plot1.pv.getPlot().setMarkerEnabled(True)
            peak_pos.value = float('NaN')
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
