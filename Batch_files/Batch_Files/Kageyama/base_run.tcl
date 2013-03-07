samplename Sample 3 at 150K
hset /sample/tc1/sensor/setpoint2 150
drive tc1_driveable 150
wait 60
runscan stth 2.75 5.2 50 time 55
#