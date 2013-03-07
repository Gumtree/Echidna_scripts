drive msd 2500
drive sc 0
sampledescription "mtth122-noPC-noSC-CF3-Ge331"
sampletitle "Al2O3"
user "UTS"
samplename "Al2O3"
title "Calibration"
#tc2 range 5
#tc2 controlsensor sensorA
#tc2 tolerance 100
#tc2 heateron 1
#drive tc2 306
#-------------
runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
#for {set i 25} {$i <= 300} {incr i 25} {
#samplename [concat "NiFe2O4 4h, " $i "K"]
#drive tc1 [expr $i]
#wait 1200
#runscan stth 4 5.2 25 time 120
#}
#to switch compressor off
#tc1_asyncq send "RELAY 2,2,1" 
