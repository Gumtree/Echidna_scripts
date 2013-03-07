title P2033
sampledescription mtth140-noPC-noSC-CF7-Ge331
user Jessica Hudspeth, Darren Goossens
sampletitle ""

hset sample/tc1/heater/heaterrange_1 3
hset sample/tc1/heater/heaterrange_2 3

hset sample/tc1/control/tolerance1 2.0
hset sample/tc1/control/tolerance2 2.0

set templist [list 20 223 334 373 450]
foreach temperature $templist {
drive tc1_driveable $temperature tc1_driveable2 $temperature
wait 600
samplename [concat TGS noPC-noSC-9mm 2.44A, $temperature K ]
runscan stth 2.75 5.2 50 time 298
runscan stth 2.75 5.2 50 time 298
}
