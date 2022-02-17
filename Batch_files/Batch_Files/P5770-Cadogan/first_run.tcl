# Trying to control cooling
drive tc1_temp0_setpoint 13
hset /sample/tc1/pres3/setpoint 5
foreach one_temp { 1.5 8 40 } {
	drive tc1_temp0_setpoint $one_temp
	samplename [ concat ErTi2Ga4 at $one_temp ]
	wait 900
	runscan stth 2.75 5.2 50 time 275
}