user "Vanessa Peterson"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-335"

tc2 range 5
hset sample/tc1/heater/heaterRange_1 4
hset sample/tc1/heater/heaterRange_2 4

title P604 Ni_d4_pz_acetone_190K
drive tc1_driveable 190 tc1_driveable2 190
runscan stth -1 5.2 125 time 248

title P604 Ni_d4_pz_acetone_350K
drive tc1_driveable 350 tc1_driveable2 350
run tc2 250
runscan stth -1 5.2 125 time 248



