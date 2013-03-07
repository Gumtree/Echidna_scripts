hset sample/tc1/control/tolerance1 1
hset sample/tc1/control/tolerance2 1

hset sample/tc1/heater/heaterrange_1 3
hset sample/tc1/heater/heaterrange_2 3

drive tc1_driveable $temperature tc1_driveable2 $temperature
samplename Ba2CuTeO6 our sample, BaseTemp
runscan stth 4 5.2 25 time 550

set templist [list 20 50 80 90 100 120 150 200 300]
foreach temperature $templist {
drive tc1_driveable $temperature tc1_driveable2 $temperature
wait 600
samplename [concat Ba2CuTeO6, $temperature K ]
runscan stth 4 5.2 25 time 550
}
