# Automatic cooldown
#
# 
drive tc1_driveable 20
hset /sample/pc1/setpoint 4
drive tc1_driveable 1.5
samplename FTO_at_base
wait 900
runscan stth 2.75 5.2 50 time 203
