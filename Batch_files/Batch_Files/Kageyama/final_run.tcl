# Now run at 300
samplename Sample 20 at 300K
hset /sample/tc1/sensor/setpoint2 300
drive tc1_driveable 300
wait 300
runscan stth 2.75 5.2 50 time 95