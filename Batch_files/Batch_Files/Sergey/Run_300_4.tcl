title Proposal 1239
sampledescription mtth140-noPC-noSC-TopLoader-Ge337
user Sergey Danilkin
sampletitle Cu1.98Se
#-----------------------------------
#Ge337 reflection 1.3A
drive mom 60.8
drive mchi -0.1
drive mf1 0.28
#-----------------------------------
hset sample/tc2/control/tolerance1 2
hset sample/tc1/control/tolerance1 2
hset sample/tc1/control/tolerance2 2

hset sample/tc2/heater/heaterRange 5
hset sample/tc1/heater/heaterRange_1 3
hset sample/tc1/heater/heaterRange_2 3
#-----------------------------------
#hset sample/tc1/sensor/setpoint1 300
#drive tc1_driveable2 300
#wait 600
samplename Cu1.98Se 295K
runscan stth 4.0 5.2 25 time 262
samplename Cu1.98Se 295K Run 2
runscan stth 4.0 5.2 25 time 262
#-----------------------------------
hset sample/tc1/sensor/setpoint1 200
drive tc1_driveable2 200
wait 600
samplename Cu1.98Se 200K
runscan stth 4.0 5.2 25 time 262
samplename Cu1.98Se 200K (Run 2)
runscan stth 4.0 5.2 25 time 262
#-----------------------------------
#---------------------------------
hset sample/tc1/sensor/setpoint1 4
drive tc1_driveable2 4