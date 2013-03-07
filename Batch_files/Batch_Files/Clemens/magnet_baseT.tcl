title Proposal 1337
sampledescription mtth140-noPC-noSC-Ge331
user Clemens Ulrich
drive sc 0
drive msd 2500

hset sample/tc2/control/tolerance1 2
hset sample/tc2/heater/heaterRange 5
hset sample/tc2/sensor/setpoint1 6
drive tc2_driveable2 6

#--------------------------------

magnet send s 7.0
samplename FeCr2S4 base T 7.0T
runscan stth 4.0 5.2 25 time 226

magnet send s 2.0
wait 600
samplename FeCr2S4 base T 2.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

magnet send s 5.0
wait 600
samplename FeCr2S4 base T 5.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226

magnet send s 6.0
wait 600
samplename FeCr2S4 base T 6.0T
runscan stth 4.0 5.2 25 time 226
runscan stth 4.0 5.2 25 time 226