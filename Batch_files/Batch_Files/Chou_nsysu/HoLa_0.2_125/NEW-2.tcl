title Proposal 654
sampledescription mtth140-noPC-noSC-TopLoader-Ge331-lamda2.439
user H. Chou
sampletitle HoLa-0.2_125

#
#tc2 tolerance 100
#tc2 controlsensor sensorA
#tc2 range 5
#tc2 heateron 0
#

tc2 heateron 1
hset /sample/tc1/heater/heaterRange_1 2
hset /sample/tc1/heater/heaterRange_2 2




drive tc2 29
drive tc1_driveable1 33 tc1_driveable2 33
samplename Ho0.8La0.2Mn2O5-33K-1
runscan stth 4.0 5.2 25 time 406

drive tc2 41
drive tc1_driveable1 45 tc1_driveable2 45
wait 1200
samplename Ho0.8La0.2Mn2O5-45K
runscan stth 4.0 5.2 25 time 406

drive tc2 56
drive tc1_driveable1 60 tc1_driveable2 60
wait 1200
samplename Ho0.8La0.2Mn2O5-60K
runscan stth 4.0 5.2 25 time 406

drive tc2 69.0
drive tc1_driveable1 73 tc1_driveable2 73
wait 1200
samplename Ho0.8La0.2Mn2O5-73K
runscan stth 4.0 5.2 25 time 406

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3
drive tc2 87
drive tc1_driveable1 90 tc1_driveable2 90
wait 300
hset /sample/tc1/heater/heaterRange_1 2
hset /sample/tc1/heater/heaterRange_2 2
wait 900
samplename Ho0.8La0.2Mn2O5-90K
runscan stth 4.0 5.2 25 time 406

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3
drive tc2 92
drive tc1_driveable1 95 tc1_driveable2 95
wait 300
hset /sample/tc1/heater/heaterRange_1 2
hset /sample/tc1/heater/heaterRange_2 2
wait 900
samplename Ho0.8La0.2Mn2O5-95K
runscan stth 4.0 5.2 25 time 406

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3
drive tc2 97
drive tc1_driveable1 100 tc1_driveable2 100
wait 300
hset /sample/tc1/heater/heaterRange_1 2
hset /sample/tc1/heater/heaterRange_2 2
wait 900
samplename Ho0.8La0.2Mn2O5-100K
runscan stth 4.0 5.2 25 time 406

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3
drive tc2 107
drive tc1_driveable1 110 tc1_driveable2 110
wait 300
hset /sample/tc1/heater/heaterRange_1 2
hset /sample/tc1/heater/heaterRange_2 2
wait 900
samplename Ho0.8La0.2Mn2O5-110K
runscan stth 4.0 5.2 25 time 406

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3
drive tc2 117
drive tc1_driveable1 120 tc1_driveable2 120
wait 300
wait 900
samplename Ho0.8La0.2Mn2O5-120K
runscan stth 4.0 5.2 25 time 406


drive tc2 127
drive tc1_driveable1 130 tc1_driveable2 130
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-130K
runscan stth 4.0 5.2 25 time 406


drive tc2 137
drive tc1_driveable1 140 tc1_driveable2 140
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-140K
runscan stth 4.0 5.2 25 time 406


drive tc2 142
drive tc1_driveable1 145 tc1_driveable2 145
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-145K
runscan stth 4.0 5.2 25 time 406


drive tc2 147
drive tc1_driveable1 150 tc1_driveable2 150
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-150K
runscan stth 4.0 5.2 25 time 406

drive tc2 157
drive tc1_driveable1 160 tc1_driveable2 160
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-160K
runscan stth 4.0 5.2 25 time 406


drive tc2 177
drive tc1_driveable1 180 tc1_driveable2 180
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-180K
runscan stth 4.0 5.2 25 time 406

drive tc2 197
drive tc1_driveable1 200 tc1_driveable2 200
wait 300
wait 900
samplename Ho0.8La0.2Mn2O5-200K
runscan stth 4.0 5.2 25 time 406


drive tc2 247
drive tc1_driveable1 250 tc1_driveable2 250
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-250K
runscan stth 4.0 5.2 25 time 406


drive tc2 297
drive tc1_driveable1 300 tc1_driveable2 300
wait 300

wait 900
samplename Ho0.8La0.2Mn2O5-300K
runscan stth 4.0 5.2 25 time 406

#for {set i 100} {$i <= 300} {incr i 100} {
#drive tc2 [expr $i]
#drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
#wait 1200
#samplename [concat Bi0.9Pb0.1FeO3, $i K ]
#runscan stth 4.0 5.2 25 time 550

#
# After 400 we don't use the cold head heater in order to
# protect the Si diode (max 475K)
#
#hset /sample/tc1/heater/heaterRange_1 3
#
#for {set i 400} {$i <= 600} {incr i 100} {
#drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
#wait 1800
#samplename [concat Bi0.9Pb0.1FeO3, $i K ]
#runscan stth 4.0 5.2 25 time 262
#}

#for {set i 700} {$i <= 800} {incr i 20} {
#drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
#wait 1800
#samplename [concat Bi0.9Pb0.1FeO3, $i K ]
#runscan stth 4.0 5.2 25 time 262
#}
tc2 heateron 0
drive tc1_driveable 293 tc1_driveable2 293