# Create scripts for running on Echidna
# Setup area
__script__.title = "Create SICS script"
__script__.version = "0.1"
# Overall information
equipment = {"CF7/8":'cf',"Vacuum Furnace":'vf'}
overall_equipment = Par('string','CF7/8', options= equipment.keys())
overall_equipment.title = 'Ancillary'
overall_sample = Par('string','<sample_name_here>')
overall_sample.title = 'Sample name'
overall_overlaps = Par('int','1')
overall_overlaps.title = 'Overlaps'
overall_stepsize = Par('float','0.05',options=('0.125','0.05'))
overall_stepsize.title = "Step size"
Group('Equipment').add(overall_equipment,overall_sample,overall_overlaps,overall_stepsize)
# Temperatures
temper_entry = Par('string','4')
temper_entry.title = "Temperatures"
temper_gen = Act('temper_gen_proc()','Generate temperatures')
temper_gen_start = Par('float','4.0')
temper_gen_start.title = "Start"
temper_gen_step = Par('float','10.0')
temper_gen_step.title = "Step"
temper_gen_stop = Par('float','200.0')
temper_gen_stop.title = "Finish"
temper_gen_replace = Par('string','Replace',options=('Replace','Append'))
temper_gen_replace.title = "Replace/Append"
Group('Temperatures').add(temper_entry,temper_gen_start,temper_gen_step,temper_gen_stop,temper_gen_replace,temper_gen)
# Times
time_entry = Par('string','275')
time_entry.title = "Measurement time"
time_gen = Act('time_gen_proc()','Generate times')
time_new = Par('int','275')
time_new.title = "Additional time"
time_gen_num = Par('int','5')
time_gen_num.title = "Repeats"
time_gen_replace = Par('string','Replace',options=['Replace','Append'])
time_gen_replace.title = "Replace/Append new times"
Group('Measurement times').add(time_entry,time_new,time_gen_num,time_gen_replace,time_gen)
# Options
options_wait = Par('bool','false')
options_wait.title = "Wait for beam"
options_temp_wait = Par('int','300')
options_temp_wait.title = "Wait for equilibration"
options_ramp = Par('float','0.0')
options_ramp.title = "Ramp rate"
options_sensor_bot = Par('bool','true')
options_sensor_bot.title = "Control on bottom sensor\nas well (CF only)"
Group('Options').add(options_wait,options_temp_wait,options_ramp,options_sensor_bot)
# Make it happen
output_dir = Par('file')
output_dir.dtype = 'folder'
output_dir.title = "Output Directory"
output_name = Par('string')
output_name.title = "Script name"
output_script = Act('generate_script()',"Generate script")
output_calc = Act('calculate_total_time()',"Calculate total time")
Group('Output').add(output_dir,output_name,output_calc,output_script)

def temper_gen_proc():
    start = float(temper_gen_start.value)
    step = float(temper_gen_step.value)
    stop = float(temper_gen_stop.value)
    outstring = ""
    t = start
    while t <= stop:
        outstring += " %.1f " % t
        t = t + step
    if str(temper_gen_replace.value) == 'Replace':
        temper_entry.value = outstring
    elif str(temper_gen_replace.value) == 'Append':
        temper_entry.value += outstring

def time_gen_proc():
    timeval = int(time_new.value)
    rpts = int(time_gen_num.value)
    apprep = str(time_gen_replace.value)
    new_string = rpts *( "%d " %timeval)
    if apprep == 'Replace':
        time_entry.value = new_string
    elif apprep == 'Append':
        time_entry.value += " "+new_string

def calculate_total_time():
    print "Calculating time"
    all_times = str(time_entry.value).split()
    num_temps = len(str(temper_entry.value).split())
    wait_time = int(options_temp_wait.value)
    all_times = map(int,all_times)
    overlaps = int(overall_overlaps.value)
    steps = 1.25/float(overall_stepsize.value)
    total_time = 0
    if len(all_times) == 1:
        total_time = (time_for_scan(steps,overlaps,all_times[0])+wait_time)*num_temps
    else:
        for t in all_times:
            total_time += time_for_scan(steps,overlaps,t) + wait_time
    open_error( "Total time %d secs = %f hours = %f days" % (total_time, total_time/3600, total_time/3600/24))

def time_for_scan(steps,overlaps,dwelltime):
    return steps*(dwelltime+13)*(overlaps+1)

def generate_script():
    # Only CF7 at the moment
    scancmd = generate_scan_cmd(float(overall_stepsize.value),int(overall_overlaps.value))
    all_times = str(time_entry.value).split()
    num_temps = len(str(temper_entry.value).split())
    if len(all_times) > 1 and len(all_times) != num_temps:
        open_error("Number of times does not match number of temperatures")
        return
    samp_name = "samplename [concat %s at $tempval K]" % str(overall_sample.value)
    time_list = "[ "
    if len(all_times) == 1:
        time_val = str(time_entry.value).strip()
        for i in range(0,num_temps):
           time_list +="%s " % str(time_entry.value)
    else:
        time_list += str(time_entry.value)
    time_list += " ]"
    temp_list = "[ " + str(temper_entry.value) + " ]"
    full_script = cf7_template() % (temp_list,time_list,samp_name,"",str(options_temp_wait.value),scancmd)
    print full_script


def generate_scan_cmd(stepsize,overlaps):
    start = 4.0 - 1.25*overlaps
    if stepsize == 0.05:
        finish = 5.2
    else:
        finish = 5.125
    numsteps = int(round(1.25/stepsize)) * (overlaps + 1)
    return "runscan stth %.2f %.3f %d time $timeval\n" % (start,finish,numsteps)

def cf7_template():
    template = """

set templist %s
set timelist %s

foreach tempval $templist timeval $timelist {
    %s
    drive tc1_driveable $tempval %s
    wait %s
    %s
}
    """
    return template
