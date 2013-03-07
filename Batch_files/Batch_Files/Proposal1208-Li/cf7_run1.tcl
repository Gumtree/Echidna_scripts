title Proposal 1208
sampledescription mtth140-noPC-noSC-TopLoader-Ge335
user W. H. Li
sampletitle Bi0.95Pb0.05FeO3
#
#
# set up heating loops
#
#tc2 tolerance 100
#tc2 controlsensor sensorA
#tc2 range 5
#tc2 heateron 0
#
#samplename Bi0.95Pb0.05FeO3 cooling
#runscan stth 4.0 5.2 25 time 118
#
#drive tc1_driveable2 5
#
#samplename Bi0.95Pb0.05FeO3 at base
#runscan stth 4.0 5.2 25 time 550
#
#tc2 heateron 1
#hset /sample/tc1/heater/heaterRange_2 3
#
for {set i 50} {$i <= 350} {incr i 50} {
drive tc2 [expr $i] tc1_driveable2 [expr $i]
wait 1200
samplename [concat Bi0.95Pb0.05FeO3, $i K ]
runscan stth 4.0 5.2 25 time 550
}
#
# After 400 we don't use the cold head heater in order to
# protect the Si diode (max 475K)
#
hset /sample/tc1/heater/heaterRange_1 3
#
for {set i 350} {$i <= 700} {incr i 50} {
drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
wait 1800
samplename [concat Bi0.95Pb0.05FeO3, $i K ]
runscan stth 4.0 5.2 25 time 550
}
#
tc2 heateron 0
drive tc1_driveable 293 tc1_driveable2 293
