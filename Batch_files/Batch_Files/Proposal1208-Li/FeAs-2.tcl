title Proposal 1208
sampledescription mtth140-noPC-noSC-TopLoader-Ge331
user W. H. Li
sampletitle FeAs/FeAs2

tc2 tolerance 200
tc2 controlsensor sensorA
tc2 range 5
#tc2 heateron 0
tc2 heateron 1

hset /sample/tc1/heater/heaterRange_1 2
hset /sample/tc1/heater/heaterRange_2 2
hset sample/tc1/control/tolerance 1.5

drive tc2 3
drive tc1_driveable 3 tc1_driveable2 3
wait 120
samplename FeAs/FeAs2 base T
runscan stth 4.0 5.2 25 time 406

drive tc2 46
drive tc1_driveable 50 tc1_driveable2 50
wait 120
samplename FeAs/FeAs2 50K
runscan stth 4.0 5.2 25 time 406

drive tc2 96
drive tc1_driveable 100 tc1_driveable2 100
wait 120
samplename FeAs/FeAs2 100K
runscan stth 4.0 5.2 25 time 406

drive tc2 146
drive tc1_driveable 150 tc1_driveable2 150
wait 120
samplename FeAs/FeAs2 150K
runscan stth 4.0 5.2 25 time 406

drive tc2 196
drive tc1_driveable 200 tc1_driveable2 200
wait 120
samplename FeAs/FeAs2 200K
runscan stth 4.0 5.2 25 time 406

drive tc2 296
drive tc1_driveable 300 tc1_driveable2 300
wait 120
samplename FeAs/FeAs2 300K
runscan stth 4.0 5.2 25 time 406

tc2 heateron 0
drive tc1_driveable 293 tc1_driveable2 293
