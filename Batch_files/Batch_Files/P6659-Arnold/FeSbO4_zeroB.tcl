# Trying to control cooling
drive tc1_temp0_setpoint 10
hset /sample/tc1/pres8/setpoint 5
drive tc1_temp0_setpoint 1.5
# Wait for a bit
wait 900
samplename FeSbO4_1pt5K
runscan stth 2.75 5.2 50 time 851
#
foreach one_temp { 10 } {
	drive tc1_temp0_setpoint $one_temp
	samplename [ concat FeSbO4 at $one_temp ]
	wait 900
	runscan stth 2.75 5.2 50 time 275
}