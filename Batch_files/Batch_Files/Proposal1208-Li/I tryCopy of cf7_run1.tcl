title Proposal 1208
sampledescription mtth140-noPC-noSC-TopLoader-Ge335
user W. H. Li
sampletitle Bi0.95Pb0.05FeO3


#
# After 400 we don't use the cold head heater in order to
# protect the Si diode (max 475K)
#
hset /sample/tc1/heater/heaterRange_1 3
#
samplename "Bi0.95Pb0.05FeO3 250 K"
runscan stth 4.0 5.2 25 time 406

for {set i 350} {$i <= 550} {incr i 100} {
drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
wait 1800
samplename [concat Bi0.95Pb0.05FeO3, $i K ]
runscan stth 4.0 5.2 25 time 406
}
#
for {set i 600} {$i <= 700} {incr i 20} {
drive tc1_driveable [expr $i] tc1_driveable2 [expr $i]
wait 1200
samplename [concat Bi0.95Pb0.05FeO3, $i K ]
runscan stth 4.0 5.2 25 time 406
}
tc2 heateron 0
drive tc1_driveable 293 tc1_driveable2 293
