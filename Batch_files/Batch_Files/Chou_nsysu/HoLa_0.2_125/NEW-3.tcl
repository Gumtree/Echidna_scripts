title Proposal 654
sampledescription mtth140-noPC-noSC-TopLoader-Ge331-lamda2.439
user H. Chou
sampletitle HoLa-0.2_125

#
tc2 tolerance 200
#tc2 controlsensor sensorA
tc2 range 5
#tc2 heateron 0


##tc2 heateron 1
##hset /sample/tc1/heater/heaterRange_1 2
##hset /sample/tc1/heater/heaterRange_2 2
##hset sample/tc1/control/tolerance 1.5

##drive tc2 4
##drive tc1_driveable 5 tc1_driveable2 5
##wait 120
##samplename Ho0.8La0.2Mn2O5-5K-a
##runscan stth 4.0 5.2 25 time 406

##drive tc2 16
##drive tc1_driveable 20 tc1_driveable2 20
##wait 120
##samplename Ho0.8La0.2Mn2O5-20K-a
##runscan stth 4.0 5.2 25 time 406

##drive tc2 29
##drive tc1_driveable 33 tc1_driveable2 33
##wait 120
##samplename Ho0.8La0.2Mn2O5-33K-a
##runscan stth 4.0 5.2 25 time 406

##drive tc2 41
##drive tc1_driveable 45 tc1_driveable2 45
##wait 120
##samplename Ho0.8La0.2Mn2O5-45K-a
##runscan stth 4.0 5.2 25 time 406

##drive tc2 56
##drive tc1_driveable 60 tc1_driveable2 60
##wait 120
##samplename Ho0.8La0.2Mn2O5-60K-a
##runscan stth 4.0 5.2 25 time 406

##drive tc2 69
##drive tc1_driveable 73 tc1_driveable2 73
##wait 120
##samplename Ho0.8La0.2Mn2O5-73K-a
##runscan stth 4.0 5.2 25 time 406


drive tc2 86
drive tc1_driveable 90 tc1_driveable2 90
wait 120
samplename Ho0.8La0.2Mn2O5-90K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 91
drive tc1_driveable 95 tc1_driveable2 95
wait 120
samplename Ho0.8La0.2Mn2O5-95K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 96
drive tc1_driveable 100 tc1_driveable2 100
wait 120
samplename Ho0.8La0.2Mn2O5-100K-a
runscan stth 4.0 5.2 25 time 406

hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3

drive tc2 106
drive tc1_driveable 110 tc1_driveable2 110
wait 120
samplename Ho0.8La0.2Mn2O5-110K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 116
drive tc1_driveable 120 tc1_driveable2 120
wait 120
samplename Ho0.8La0.2Mn2O5-120K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 126
drive tc1_driveable 130 tc1_driveable2 130
wait 120
samplename Ho0.8La0.2Mn2O5-130K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 136
drive tc1_driveable 140 tc1_driveable2 140
wait 120
samplename Ho0.8La0.2Mn2O5-140K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 141
drive tc1_driveable 145 tc1_driveable2 145
wait 120
samplename Ho0.8La0.2Mn2O5-145K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 146
drive tc1_driveable 150 tc1_driveable2 150
wait 120
samplename Ho0.8La0.2Mn2O5-150K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 156
drive tc1_driveable 160 tc1_driveable2 160
wait 120
samplename Ho0.8La0.2Mn2O5-160K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 176
drive tc1_driveable 180 tc1_driveable2 180
wait 120
samplename Ho0.8La0.2Mn2O5-180K-a
runscan stth 4.0 5.2 25 time 406

drive tc2 196
drive tc1_driveable 200 tc1_driveable2 200
wait 120
samplename Ho0.8La0.2Mn2O5-200K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 246
drive tc1_driveable 250 tc1_driveable2 250
wait 120
samplename Ho0.8La0.2Mn2O5-250K-a
runscan stth 4.0 5.2 25 time 406


drive tc2 296
drive tc1_driveable 300 tc1_driveable2 300
wait 120
samplename Ho0.8La0.2Mn2O5-300K-a
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