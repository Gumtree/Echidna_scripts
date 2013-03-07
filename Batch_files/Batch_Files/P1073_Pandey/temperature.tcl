hset /sample/tc1/heater/heaterRange_1 5
hset /sample/tc1/heater/heaterRange_2 5
#
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4
# cooling down scan
samplename PSZT during cooling
runscan stth 4.0 5.2 25 time 118
drive tc1_driveable 4
# proper scan
samplename PSZT at base (4K)
runscan stth 4.0 5.2 25 time 550
#
hset /sample/tc1/sensor/setpoint2 300
drive tc1_driveable 300
wait 300
samplename PSZT at 300K
runscan stth 4.0 5.2 25 time 550