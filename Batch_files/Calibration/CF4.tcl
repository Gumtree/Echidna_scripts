drive msd 2500
drive sc 1
sampledescription "mtth120-PC10-SC10-CF4"
sampletitle ""
user "Brendan Kennedy"
samplename "Bi4Ti3O12"
title "Proposal"
tc1 range 5
tc1 controlsensor sensorB
tc1 tolerance 100
tc1 heateron 0
#-------------
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 118
runscan stth 2.75 5.2 50 time 406
tc1 heateron 1
drive tc1 50
runscan stth 4 5.2 25 time 118
runscan stth 2.75 5.2 50 time 406
tc1 heateron 1
drive tc1 100
runscan stth 4 5.2 25 time 118
runscan stth 2.75 5.2 50 time 406
tc1 heateron 1
drive tc1 200
runscan stth 4 5.2 25 time 118
runscan stth 4 5.2 25 time 118
runscan stth 2.75 5.2 50 time 406
drive tc1 300
runscan stth 4 5.2 25 time 118
runscan stth 4 5.2 25 time 118
runscan stth 2.75 5.2 50 time 406
#to switch compressor off
#tc1_asyncq send "RELAY 2,2,1"
