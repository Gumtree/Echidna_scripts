sampledescription mtth140-noPC-noSC-CF10-Ge331
user J. S. Gardner, J-Y Lin, C.-W. Wang
sampletitle (HoCa)2Ti2O7
#hset sample/tc2/heater/heaterrange_1 3
#hset sample/tc1/heater/heaterrange_1 3
#hset sample/tc1/heater/heaterrange_2 3

#hset sample/tc1/control/tolerance1 5
#hset sample/tc1/control/tolerance2 5

drive mom 106.55
drive mchi -0.7
drive mf1 0.3
runscan stth 2.75 5.2 1 time 3000 force true
runscan stth 2.75 5.2 1 MONITOR_3 200000 force true

sampledescription mtth140-noPC-noSC-CF10-Ge331
samplename Ho1.97Ca0.03Ti2O7 noPC-noSC-Cu can-2.4 A, at base
runscan stth 2.75 5.2 50 MONITOR_3 400000

run mom 70.14
run mchi -0.255
run mf1 0.264
run mom 70.14
run mchi -0.255
run mf1 0.264
sampledescription mtth140-noPC-noSC-CF10-Ge335
samplename Ho1.97Ca0.03Ti2O7 noPC-noSC-Cu can-1.6 A, at base K,
runscan stth 2.75 5.125 50 time 120

