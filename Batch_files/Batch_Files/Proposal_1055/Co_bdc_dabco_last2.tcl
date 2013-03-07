user "Vanessa Peterson"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-331"

#tc2 range 5
#hset sample/tc1/heater/heaterRange_1 4
#hset sample/tc1/heater/heaterRange_2 4

title P1055 Co_bdc_dabco_130K
#drive tc1_driveable 130 tc1_driveable2 130
#drive tc2 130
wait 120
drive tc1_driveable 130 tc1_driveable2 130
drive tc2 130
runscan stth 1.5 5.2 75 time 454

title P1055 Co_bdc_dabco_160K
drive tc1_driveable 160 tc1_driveable2 160
drive tc2 160
wait 120
drive tc1_driveable 160 tc1_driveable2 160
drive tc2 160
runscan stth 1.5 5.2 75 time 454
