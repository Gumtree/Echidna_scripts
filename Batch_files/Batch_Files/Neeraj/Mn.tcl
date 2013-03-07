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
drive tc2 3
drive tc1_driveable 3
wait 600
samplename Mn base T
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 14
drive tc1_driveable 14
wait 600
samplename Mn 14K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 24
drive tc1_driveable 24
wait 600
samplename Mn 24K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 34
drive tc1_driveable 34
wait 600
samplename Mn 34K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 44
drive tc1_driveable 44
wait 600
samplename Mn 44K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 54
drive tc1_driveable 54
wait 600
samplename Mn 54K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 64
drive tc1_driveable 64
wait 600
samplename Mn 64K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 74
drive tc1_driveable 74
wait 600
samplename Mn 74K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 84
drive tc1_driveable 84
wait 600
samplename Mn 84K
runscan stth 2.75 5.2 50 time 118
#-------------------------
drive tc2 94
drive tc1_driveable 94
wait 600
samplename Mn 94K
runscan stth 2.75 5.2 50 time 118
#-------------------------
hset sample/tc1/sensor/setpoint1 3
drive tc2 3
drive tc1_driveable 3
