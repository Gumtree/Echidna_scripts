# run at base temperature
drive tc1_driveable2 10
samplename SBFO0_2 at 10K
runscan stth 2.75 5.2 50 time 334
# run at 150 K
hset /sample/tc2/sensor/setpoint1 150
drive tc1_driveable2 150
samplename SBFO0_2 at 150K
runscan stth 2.75 5.2 50 time 154