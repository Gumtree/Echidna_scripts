# Sequence of temperatures using top loader and Lakeshore 336
title P1350
sampledescription mtth140-noPC-noSC-CF7-Ge335
user Neeraj Sharma
#-------------------------
tc2 tolerance 2
tc2 controlsensor sensorA
tc2 range 5
#tc2 heateron 0
tc2 heateron 1
hset /sample/tc1/heater/heaterRange_1 3
#hset /sample/tc1/heater/heaterRange_2 2
hset sample/tc1/control/tolerance 1
#-------------------------
for {set i 4} {$i <= 94} {incr i 10} {
drive tc2 $i
drive tc1_driveable [expr $i]
wait 600
samplename [concat Fe, $i K ]
runscan stth 2.75 5.2 50 time 118
}
tc2 heateron 0
drive tc1_driveable 3
