user "Vanessa Peterson"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-335"

tc2 range 5
hset sample/tc1/heater/heaterRange_1 4
hset sample/tc1/heater/heaterRange_2 4

title P604 Pt_d4_pz_acetone_180K
run tc2 150
drive tc1_driveable 180 tc1_driveable2 180
runscan stth -1 5.2 125 time 176

title P604 Pt_d4_pz_acetone_320K
drive tc1_driveable 320 tc1_driveable2 320
run tc2 250
runscan stth -1 5.2 125 time 176
run tc2 150
run tc1_driveable 190 tc1_driveable2 190
