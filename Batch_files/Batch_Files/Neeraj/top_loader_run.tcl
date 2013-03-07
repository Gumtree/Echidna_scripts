title Proposal 1168
sampledescription mtth140-noPC-SC10-Ge335
user Will Brant / Siegbert / Neeraj / James	

tc2 range 5
drive tc2 6
hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/sensor/setpoint1 6
wait 300
#
drive sc 1
drive msd 2500
#
# At base of 5K
#
samplename LSTN1_Chem,6K/1.622A
runscan stth 2.75 5.2 50 time 622

#
# Warm up to 300K
#
#
tc2 range 5
hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/sensor/setpoint1 300
drive tc2 300
wait 300
samplename  LSTN1_Chem,300K/1.622A
runscan stth 2.75 5.2 50 time 262