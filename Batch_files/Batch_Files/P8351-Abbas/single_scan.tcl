samplename NiO_nano_14nm 100K
runscan stth 2.75 5.125 20 time 1787
#
hset /sample/tc2/sensor/setpoint1 30
drive tc1_driveable 50
drive tc2_driveable 30
samplename NiO_nano_14nm_50K
wait 300
runscan stth 2.75 5.125 20 time 1787
#