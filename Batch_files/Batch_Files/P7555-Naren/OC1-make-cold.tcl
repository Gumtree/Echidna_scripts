# Cool down OC1
#hset /sample/pc1/setpoint 20
#samplename CrTaO during cooling in OC
#runscan stth 2.75 5.125 20 time 50 
#drive tc1_driveable 15
#
#hset /sample/pc1/setpoint 4
#hset /sample/tc1/setpoint 1.5
#wait 900
#
samplename CrTaO at base
runscan stth 2.75 5.2 50 time 491
drive tc1_driveable 4
wait 900
samplename CrTaO at 4K
runscan stth 2.75 5.2 50 time 60
#
drive tc1_driveable 12
wait 900
runscan stth 2.75 5.2 50 time 491