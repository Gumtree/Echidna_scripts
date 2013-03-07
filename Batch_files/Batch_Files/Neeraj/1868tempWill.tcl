drive msd 2500
drive sc 0
sampledescription mtth140-noPC-noSC-CF7-Ge335
user Siggi Schmid 
title Proposal 1868

#hset /sample/tc1/heater/heaterRange_1 3
#hset /sample/tc1/heater/heaterRange_2 3
#hset sample/tc1/control/tolerance 1

proc runtemps {} {
set templist [list 373 398 ]

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3

foreach temperature $templist {
samplename [ concat LSTN_Li0.28, $temperature K ]
hset /sample/tc1/sensor/setpoint2 $temperature
drive tc1_driveable $temperature
wait 600
runscan stth 2.75 5.2 50 time 190 
}
}

runtemps