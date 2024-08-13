sampledescription mtth140-noPC-noSC-CF7-Ge331
user PB, Max, CWW
sampletitle ""

hset sample/tc2/heater/heaterrange_1 3
hset sample/tc1/heater/heaterrange_1 3
hset sample/tc1/heater/heaterrange_2 3

hset sample/tc1/control/tolerance1 2
hset sample/tc1/control/tolerance2 2
#---------------------------------------
drive mom 105.1 mchi -1.74 mf1 0.31
#---------------------------------------

set templist [list 300 350 400 450 ]
foreach temperature $templist {

if {$temperature <= 300} then {
#hset sample/tc2/sensor/setpoint1 [expr $temperature - 20]
hset sample/tc2/sensor/setpoint1 [expr $temperature]
} else {
hset sample/tc2/sensor/setpoint1 300
}

#hset sample/tc2/sensor/setpoint1 $temperature
drive tc1_driveable $temperature tc1_driveable2 $temperature
wait 600
samplename [concat NaFePO4SO4 9mm-2p4A-CF7, $temperature K ]
runscan stth 2.75 5.2 50 time 260
#runscan stth 2.75 5.2 50 MONITOR_3 1750000
#runscan stth 2.75 5.125 20 time 250
}

hset sample/tc2/sensor/setpoint1 3
hset sample/tc1/sensor/setpoint1 3
hset sample/tc1/sensor/setpoint2 3
