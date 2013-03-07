# Run at base temperature
samplename ZnO 2.5 percent Nd at 150 K
hset /sample/tc1/sensor/setpoint2 150
drive tc1_driveable 150
wait 600
runscan stth 1.5 5.2 75 time 454
