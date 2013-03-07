title Proposal 1239
sampledescription mtth140-noPC-noSC-TopLoader-Ge337
user Sergey Danilkin
#---------------------------------
hset sample/tc1/sensor/setpoint1 4
drive tc1_driveable2 4
wait 600
samplename Cu1.98Se 4K
runscan stth 4.0 5.2 25 time 262
samplename Cu1.98Se 4K Run 2
runscan stth 4.0 5.2 25 time 262
#-----------------------------------
hset sample/tc1/sensor/setpoint1 430
drive tc1_driveable2 430
wait 600
samplename Cu1.98Se 430K
runscan stth 4.0 5.2 25 time 262
samplename Cu1.98Se 430K Run 2
runscan stth 4.0 5.2 25 time 262
#-----------------------------------
hset /sample/tc1/sensor/setpoint1 300
hset /sample/tc1/sensor/setpoint2 300
