title Proposal 1208
sampledescription mtth140-noPC-noSC-TopLoader-Ge335
user W. H. Li
sampletitle Bi0.95Pb0.05FeO3

#hset /sample/tc1/heater/heaterRange_1 3

#for {set i 300} {$i <= 600} {incr i 150} {
#drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
#wait 1800
#samplename [concat Bi0.95Pb0.05FeO3, $i K ]
#runscan stth 4.0 5.2 25 time 262
#}
#
for {set i 620} {$i <= 700} {incr i 20} {
drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
wait 1200
samplename [concat Bi0.95Pb0.05FeO3, $i K ]
runscan stth 4.0 5.2 25 time 406
}
#tc2 heateron 0
drive tc1_driveable 293 tc1_driveable2 293
