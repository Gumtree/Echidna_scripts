title Proposal 1208
sampledescription mtth140-noPC-noSC-TopLoader-Ge335
user W. H. Li
sampletitle FeAs/FeAs2

# set up heating loops
#
tc2 tolerance 100
tc2 controlsensor sensorA
tc2 range 5
#tc2 heateron 0
#
tc2 heateron 1
hset /sample/tc1/heater/heaterRange_2 3


#samplename FeAs at base
#runscan stth 4.0 5.2 25 time 478

#drive tc2 40
#drive tc1_driveable 40 tc1_driveable2 40
#wait 1200
#samplename FeAs 40K
#runscan stth 4.0 5.2 25 time 478


drive tc2 85
drive tc1_driveable 85 tc1_driveable2 85
wait 1200
samplename FeAs 85K
runscan stth 4.0 5.2 25 time 550

drive tc2 120
drive tc1_driveable 120 tc1_driveable2 120
wait 1200
samplename FeAs 120K
runscan stth 4.0 5.2 25 time 550

drive tc2 150
drive tc1_driveable 150 tc1_driveable2 150
wait 1200
samplename FeAs 150K
runscan stth 4.0 5.2 25 time 550


drive tc2 200
drive tc1_driveable 200 tc1_driveable2 200
wait 1200
samplename FeAs 200K
runscan stth 4.0 5.2 25 time 550

drive tc1_driveable 293 tc1_driveable2 293
wait 1200
samplename FeAs 293K
runscan stth 4.0 5.2 25 time 550


#for {set i 100} {$i <= 300} {incr i 100} {
#drive tc2 [expr $i]
#drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
#wait 1200
#samplename [concat Bi0.9Pb0.1FeO3, $i K ]
#runscan stth 4.0 5.2 25 time 550
}
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