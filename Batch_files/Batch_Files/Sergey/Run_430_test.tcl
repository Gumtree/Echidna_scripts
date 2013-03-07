title Proposal 1239
sampledescription mtth140-noPC-noSC-TopLoader-Ge337
user Sergey Danilkin
#-----------------------------------
hset sample/tc2/control/tolerance1 2
hset sample/tc1/control/tolerance1 2
hset sample/tc1/control/tolerance2 2

hset sample/tc2/heater/heaterRange 5
hset sample/tc1/heater/heaterRange_1 3
hset sample/tc1/heater/heaterRange_2 3
#-----------------------------------
hset sample/tc1/sensor/setpoint1 430
drive tc1_driveable2 430
samplename 50PbO_D 430K short run
runscan stth 4.0 5.2 25 time 46
#-----------------------------------
