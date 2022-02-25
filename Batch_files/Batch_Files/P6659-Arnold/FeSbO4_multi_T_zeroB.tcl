#
foreach one_temp { 30 50 75 100 } {
	drive tc1_temp0_setpoint $one_temp
	samplename [ concat FeSbO4 at $one_temp ]
	wait 900
	runscan stth 2.75 5.2 50 time 275
}

# Trying to control cooling
hset /sample/tc1/pres8/setpoint 20
drive tc1_temp0_setpoint 10
hset /sample/tc1/pres8/setpoint 5
drive tc1_temp0_setpoint 1.5