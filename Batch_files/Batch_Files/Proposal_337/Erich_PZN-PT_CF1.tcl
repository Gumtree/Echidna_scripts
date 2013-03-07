drive msd 2500
drive sc 0
config rights manager ansto
sampledescription "mtth140-PC10-SC10-CF1-Ge335"
sampletitle "PZN-7%PT"
user "Erich Kisi"
title "Proposal 337"
tc1 range 5
tc1 controlsensor sensorD
tc1 tolerance 500
tc1 heateron 0
tc2 range 5
tc2 controlsensor sensorC
tc2 tolerance 500
tc2 heateron 0
#-------------
samplename "PZN-7%PT cooling"
runscan stth 4 5.2 25 time 118
runscan stth 4 5.2 25 time 118
runscan stth 4 5.2 25 time 118
samplename "PZN-7%PT base T"
runscan stth 4 5.2 25 time 694
tc1 heateron 1
tc2 heateron 1
#-------------
drive tc1 160
drive tc2 160
samplename "PZN-7%PT 160K"
wait 3600
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 230
drive tc2 230
samplename "PZN-7%PT 230K"
wait 1800
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 280
drive tc2 280
samplename "PZN-7%PT 280K"
wait 1200
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 330
drive tc2 330
samplename "PZN-7%PT 330K"
wait 1200
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 345
drive tc2 345
samplename "PZN-7%PT 345K"
wait 900
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 360
drive tc2 360
samplename "PZN-7%PT 360K"
wait 900
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 375
drive tc2 375
samplename "PZN-7%PT 375K"
wait 900
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 385
drive tc2 385
samplename "PZN-7%PT 385K"
wait 600
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 395
drive tc2 395
samplename "PZN-7%PT 395K"
wait 600
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 405
drive tc2 405
samplename "PZN-7%PT 405K"
wait 600
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 420
drive tc2 420
samplename "PZN-7%PT 420K"
wait 900
runscan stth 4 5.2 25 time 694
#-------------
drive tc1 470
drive tc2 470
samplename "PZN-7%PT 470K"
wait 1800
runscan stth 4 5.2 25 time 694

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
