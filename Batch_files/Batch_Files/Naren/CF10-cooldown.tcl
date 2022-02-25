# Automatic cooldown
#
# 
hset /sample/tc1/temp6/setpoint 20
drive tc1_temp0_setpoint 20
hset /sample/tc1/pres8/setpoint 4
drive tc1_temp6_setpoint 1.5
samplename EFWO_at_base
wait 900
runscan stth 2.75 5.2 50 time 275
