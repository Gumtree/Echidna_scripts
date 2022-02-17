hset /sample/tc2/sensor/setpoint1 3
hset /sample/tc1/sensor/setpoint1 3
hset /sample/tc1/sensor/setpoint2 3

drive tc2_driveable 4 tc1_driveable 4
wait 300

samplename LuInFeO3_at_base
runscan stth 2.75 5.2 50 time 203