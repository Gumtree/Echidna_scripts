# Sequence of temperatures using top loader and Lakeshore 336
title P1350
sampledescription mtth140-noPC-SC10-CF7-Ge331
user Neeraj Sharma
#-------------------------
tc2 tolerance 2
tc2 controlsensor sensorA
tc2 range 5
tc2 heateron 1
hset /sample/tc1/heater/heaterRange_1 3
#hset sample/tc1/control/tolerance 2
#-------------------------
#drive tc2 3
#drive tc1_driveable 3
#wait 1200
#samplename Fe 2.7A base T
#runscan stth 2.75 5.2 50 time 190
#-------------------------
#drive tc2 24
#drive tc1_driveable 24
#wait 300
#samplename Fe 2.7A 24K
#runscan stth 2.75 5.2 50 time 190
#-------------------------
#drive tc2 44
#drive tc1_driveable 44
#wait 300
#samplename Fe 2.7A 44K
#runscan stth 2.75 5.2 50 time 190
#-------------------------
#drive tc2 64
#drive tc1_driveable 64
#wait 300
#samplename Fe 2.7A 64K
#runscan stth 2.75 5.2 50 time 190
#-------------------------
#drive tc2 84
#drive tc1_driveable 84
wait 300
samplename Fe 2.7A  84K
runscan stth 2.75 5.2 50 time 190
#-------------------------
#drive tc2 104
#drive tc1_driveable 94
#wait 300
#samplename Fe 2.7A 94K
#runscan stth 2.75 5.2 50 time 46
#-------------------------
drive tc2 3
drive tc1_driveable 3
