proc MyMakeCold {} {
	hset /sample/tc2/sensor/setpoint1 4
	hset /sample/tc2/control/tolerance1 2
	hset /sample/tc1/control/tolerance1 2
	hset /sample/tc1/control/tolerance2 2
	hset /sample/tc1/sensor/setpoint2 80
	drive tc1_driveable 80
	drive tc2_driveable 75
	wait 300
}

MyMakeCold
#
samplename Fe2.2Cu0.8O4 at 80K
runscan stth 2.75 5.2 50 time 311
#
hset /sample/tc1/sensor/setpoint1 200
hset /sample/tc1/sensor/setpoint2 200
drive tc2_driveable 190
wait 300
#
samplename Fe2.2Cu0.8O4 at 200K
runscan stth 2.75 5.2 50 time 311
MyMakeCold