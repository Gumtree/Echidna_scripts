#
#
hset /sample/tc1/sensor/setpoint2 420
hset /sample/tc1/sensor/setpoint1 420
#
samplename CsBi2Ti2NbO9pt8_heating
#
runscan stth 2.75 5.125 20 time 120
runscan stth 2.75 5.125 20 time 120
runscan stth 2.75 5.125 20 time 120
runscan stth 2.75 5.125 20 time 120
runscan stth 2.75 5.125 20 time 120
#
samplename CsBi2Ti2NbO9pt8_RT_after_baking
hset /sample/tc1/sensor/setpoint2 293
hset /sample/tc2/sensor/setpoint1 263
drive tc1_driveable 293
#
runscan stth 2.75 5.2 50 time 707
#
#hset /sample/tc1/sensor/setpoint1 
#hset /sample/tc1/sensor/setpoint2 4
#drive tc2_driveable 4
