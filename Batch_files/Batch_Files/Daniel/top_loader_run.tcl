title P1125
sampledescription mtth140-noPC-SC10-Ge335
user Daniel Riley
drive sc 1
drive msd 2500

#tc2 - sample space; tc2 - stick
hset sample/tc2/control/tolerance1 1
hset sample/tc1/control/tolerance1 1
hset sample/tc1/control/tolerance2 1

hset sample/tc2/heater/heaterRange 5
hset sample/tc1/heater/heaterRange_1 3
hset sample/tc1/heater/heaterRange_2 0

#--------------------------------
drive tc1_driveable 15 tc2_driveable 15 
samplename Ti3SiC2 15K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
drive tc1_driveable 22 tc2_driveable 22 
samplename Ti3SiC2 22K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
drive tc1_driveable 29 tc2_driveable 29 
samplename Ti3SiC2 29K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
drive tc1_driveable 32 tc2_driveable 32 
samplename Ti3SiC2 32K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
drive tc1_driveable 38 tc2_driveable 38 
samplename Ti3SiC2 38K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
drive tc1_driveable 44 tc2_driveable 44 
samplename Ti3SiC2 44K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
drive tc1_driveable 50 tc2_driveable 50 
samplename Ti3SiC2 50K
runscan stth 4.0 5.2 25 time 1270
#--------------------------------
