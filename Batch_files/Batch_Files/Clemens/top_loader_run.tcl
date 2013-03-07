title Proposal 1337
sampledescription mtth140-noPC-noSC-Ge331
user Clemens Ulrich
drive sc 0
drive msd 2500

#samplename FeCr2S4 RT in CF7
#runscan stth 4.0 5.2 25 time 262

hset sample/tc2/control/tolerance1 2
hset sample/tc1/control/tolerance1 2
hset sample/tc1/control/tolerance2 2

hset sample/tc1/heater/heaterRange_1 3
hset sample/tc1/heater/heaterRange_2 3
hset sample/tc2/heater/heaterRange 5

#--------------------------------
hset sample/tc2/sensor/setpoint1 70
hset sample/tc1/sensor/setpoint1 70
drive tc1_driveable2 70
samplename FeCr2S4 70K
runscan stth 4.0 5.2 25 time 262
#--------------------------------
hset sample/tc2/sensor/setpoint1 100
hset sample/tc1/sensor/setpoint1 100
drive tc1_driveable2 100
wait 600
samplename FeCr2S4 100K
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
#--------------------------------
hset sample/tc2/sensor/setpoint1 150
hset sample/tc1/sensor/setpoint1 150
drive tc1_driveable2 150
wait 600
samplename FeCr2S4 150K
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
#--------------------------------
hset sample/tc2/sensor/setpoint1 200
hset sample/tc1/sensor/setpoint1 200
drive tc1_driveable2 200
wait 600
samplename FeCr2S4 200K
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
#--------------------------------





#tc1_driveable2 200 # tc2_driveable 200
#samplename FeCr2S4 cooling to 200K
#runscan stth 4.0 5.2 25 time 118

#drive tc1_driveable 10 tc1_driveable2 10
