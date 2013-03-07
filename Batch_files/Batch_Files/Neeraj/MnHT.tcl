# Sequence of temperatures using top loader and Lakeshore 336
title P1350
sampledescription mtth140-noPC-noSC-CF7-Ge335
user Neeraj Sharma
#-------------------------
#tc2 tolerance 2
#tc2 controlsensor sensorA
#tc2 range 5
#tc2 heateron 1
#hset /sample/tc1/heater/heaterRange_1 3
#hset sample/tc1/control/tolerance 2
#-------------------------
drive tc2 104
drive tc1_driveable 104
wait 600
samplename Mn 104K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 114
drive tc1_driveable 114
wait 600
samplename Mn 114K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 124
drive tc1_driveable 124
wait 600
samplename Mn 124K
runscan stth 2.75 5.2 50 time 118
#-------------------------
hset sample/tc1/sensor/setpoint1 3
drive tc2 3
drive tc1_driveable 3
