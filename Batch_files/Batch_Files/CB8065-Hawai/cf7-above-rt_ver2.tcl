# Collect a series of temperatures
# in the top loader

set smpname [SplitReply [samplename]]

# Finish at 650
samplename [ concat $smpname 650 ]
hset /sample/tc1/sensor/setpoint2 650
drive tc1_driveable 650
wait 10
runscan stth 2.75 5.125 20 time 437

hset /sample/tc2/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4