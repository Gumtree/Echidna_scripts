#drive msd 2500
sampledescription "mtth140-noPC-SC-CF1"
sampletitle "LuFeO4"
user "Shane Lawrence"
samplename "LuFe2O4 cooling"
title "Proposal 361"
tc1 range 5       
tc1 controlsensor sensorA
tc1 tolerance 10
tc1 heateron 0
tc2 controlsensor sensorB
tc2 tolerance 1
tc2 heateron 1
#-------------
samplename "LuFe2O4 270K(top) 1hrs"
drive tc2 270
runscan stth 4 5.2 25 time 120
#
#samplename "LuFe2O4 270K 4hrs"
#drive tc2 270 
#wait 3600
#runscan stth 4 5.2 25 time 480
#
#samplename "LuFe2O4 200K"
#drive tc2 200
#wait 1800
#runscan stth 4 5.2 25 time 120
#
#samplename "LuFe2O4 220K"
#drive tc2 220
#wait 1800
#runscan stth 4 5.2 25 time 120
#
#samplename "LuFe2O4 240K"
#drive tc2 240
#wait 1800
#runscan stth 4 5.2 25 time 120
#
#samplename "LuFe2O4 260K"
#drive tc2 260
#wait 1800
#runscan stth 4 5.2 25 time 120
#
#tc1 heateron 1
#for {set i 25} {$i <= 300} {incr i 25} {
#samplename [concat "NiFe2O4 ceramics, " $i "K"]
#drive tc1 [expr $i]
#currtime [sicstime]
#clientput [currtime] 
#wait 2700
#runscan stth 4 5.2 25 time 90
#}
#to switch compressor off
#tc1_asyncq send "RELAY 2,2,1" 
