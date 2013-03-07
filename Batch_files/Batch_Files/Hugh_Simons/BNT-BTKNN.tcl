title ""
sampledescription mtth140-noPC-noSC-CF7-Ge335
user Hugh Simons
sampletitle BNT-BT-KNN

hset sample/tc1/control/tolerance1 1
hset sample/tc2/control/tolerance1 1

hset sample/tc1/heater/heaterrange_1 3
hset sample/tc1/heater/heaterrange_2 3

#drive tc1_driveable 298 tc1_driveable2 298 
#samplename alpha 9 (9knn)
#runscan stth 2.75 5.2 50 time 190

set templist [list 298.15 323.15 453.15 623.15]
foreach temperature $templist {
drive tc1_driveable $temperature tc1_driveable2 $temperature
wait 600
samplename [concat alpha 8 (18knn), $temperature K 1.62A]
runscan stth 2.75 5.2 50 time 226
}

drive tc1_driveable 298.15 tc1_driveable2 298.15
