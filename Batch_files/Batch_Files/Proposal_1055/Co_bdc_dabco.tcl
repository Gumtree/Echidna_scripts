user "Vanessa Peterson"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-331"

tc2 range 5
hset sample/tc1/heater/heaterRange_1 4
hset sample/tc1/heater/heaterRange_2 4

title P1055 Co_bdc_dabco_4K
drive tc1_driveable 4 tc1_driveable2 4
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_20K
drive tc1_driveable 20 tc1_driveable2 20
drive tc2 20
wait 120
drive tc1_driveable 20 tc1_driveable2 20
drive tc2 20
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_40K
drive tc1_driveable 40 tc1_driveable2 40
drive tc2 40
wait 120
drive tc1_driveable 40 tc1_driveable2 40
drive tc2 40
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_60K
drive tc1_driveable 60 tc1_driveable2 60
drive tc2 60
wait 120
drive tc1_driveable 60 tc1_driveable2 60
drive tc2 60
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_80K
drive tc1_driveable 80 tc1_driveable2 80
drive tc2 80
wait 120
drive tc1_driveable 80 tc1_driveable2 80
drive tc2 80
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_100K
drive tc1_driveable 100 tc1_driveable2 100
drive tc2 100
wait 120
drive tc1_driveable 100 tc1_driveable2 100
drive tc2 100
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_130K
drive tc1_driveable 130 tc1_driveable2 130
drive tc2 130
wait 120
drive tc1_driveable 130 tc1_driveable2 130
drive tc2 130
runscan stth 1.5 5.2 75 time 358

title P1055 Co_bdc_dabco_160K
drive tc1_driveable 160 tc1_driveable2 160
drive tc2 160
wait 120
drive tc1_driveable 160 tc1_driveable2 160
drive tc2 160
runscan stth 1.5 5.2 75 time 358
