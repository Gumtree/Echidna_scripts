title Proposal 1337
sampledescription mtth140-noPC-noSC-Ge331
user Clemens Ulrich
drive sc 0
drive msd 2500

config rights manager ansto

#samplename FeCr2S4 RT in CF7
#runscan stth 4.0 5.2 25 time 262

hset sample/tc2/control/tolerance1 2
hset sample/tc2/heater/heaterRange 5

#0T Field----------------------------
hset sample/tc2/sensor/setpoint1 4
drive tc2_driveable2 4
#wait 600
samplename FeCr2S4 BaseT
#runscan stth 4.0 5.2 25 time 262
#runscan stth 4.0 5.2 25 time 262
#runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262

hset sample/tc2/sensor/setpoint1 15
drive tc2_driveable2 15
wait 600
samplename FeCr2S4 15K
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262
runscan stth 4.0 5.2 25 time 262

#Magnetic Field 3.0T-----------------
magnet send s 3.0
hset sample/tc2/sensor/setpoint1 4
drive tc2_driveable2 4
wait 600
samplename FeCr2S4 base T 3.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

hset sample/tc2/sensor/setpoint1 15
drive tc2_driveable2 15
wait 600
samplename FeCr2S4 15K 3.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

#Magnetic Field 4.5T-----------------
magnet send s 4.5
hset sample/tc2/sensor/setpoint1 4
drive tc2_driveable2 4
wait 600
samplename FeCr2S4 base T 4.5T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

#hset sample/tc2/sensor/setpoint1 15
#drive tc2_driveable2 15
#wait 600
#samplename FeCr2S4 15K 4.5T
#runscan stth 4.0 5.2 25 time 226
#runscan stth 4.0 5.2 25 time 226

#Magnetic Field 7.0T-----------------
magnet send s 7.0
hset sample/tc2/sensor/setpoint1 4
drive tc2_driveable2 4
wait 600
samplename FeCr2S4 base T 7.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

hset sample/tc2/sensor/setpoint1 15
drive tc2_driveable2 15
wait 600
samplename FeCr2S4 15K 7.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

#Magnetic Field 100K-----------------
magnet send s 7.0
hset sample/tc2/sensor/setpoint1 100
drive tc2_driveable2 100
wait 600
samplename FeCr2S4 100K 7.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

magnet send s 3.0
wait 600
samplename FeCr2S4 100K 3.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226


#0 Field 200K-----------------
magnet send s 0
hset sample/tc2/sensor/setpoint1 200
drive tc2_driveable2 200
wait 600
samplename FeCr2S4 200K
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

config rights user sydney

