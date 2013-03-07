drive msd 2500
drive sc 0
sampledescription "mtth140-npPC-noSC-CF1-Ge331"
sampletitle ""
user "Chris Ling, Catel Sebastien, Papegay Alexandre"
title "Proposal 370"
tc1 range 5
tc1 controlsensor sensorA
tc1 tolerance 500
tc1 heateron 1
tc2 range 5
tc2 controlsensor sensorA
tc2 tolerance 500
tc2 heateron 0
#-------------
samplename "NS65MO cooling"
runscan stth 4 5.2 25 time 46
samplename "NS65MO base T"
runscan stth 4 5.2 25 time 118
runscan stth 4 5.2 25 time 550
tc1 heateron 1
tc2 heateron 1
#-------------
drive tc1 370
drive tc2 370
samplename "NS57MO 370K"
runscan stth 4 5.2 25 time 10
runscan stth 4 5.2 25 time 262
#-------------
drive tc1 380
drive tc2 380
samplename "NS57MO 380K"
runscan stth 4 5.2 25 time 10
runscan stth 4 5.2 25 time 262
#-------------
drive tc1 390
drive tc2 390
samplename "NS57MO 390K"
runscan stth 4 5.2 25 time 10
runscan stth 4 5.2 25 time 262
#-------------
drive tc1 400
drive tc2 400
samplename "NS57MO 400K"
runscan stth 4 5.2 25 time 10
runscan stth 4 5.2 25 time 262
#------------
drive tc1 100
drive tc2 100
samplename "NS57MO 100K"
runscan stth 4 5.2 25 time 46
runscan stth 4 5.2 25 time 46
runscan stth 4 5.2 25 time 262
#------------
drive tc1 200
drive tc2 200
samplename "NS57MO 200K"
runscan stth 4 5.2 25 time 46
runscan stth 4 5.2 25 time 46
runscan stth 4 5.2 25 time 262
#------------
#drive tc1 278
#drive tc2 278
#samplename "NS65MO 278K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 118
#------------
#drive tc1 280
#drive tc2 280
#samplename "NS65MO 280K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 118
#------------
#drive tc1 282
#drive tc2 282
#samplename "NS65MO 282K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 118
#------------
#drive tc1 284
#drive tc2 284
#samplename "NS65MO 284K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 118
#------------
#drive tc1 286
#drive tc2 286
#samplename "NS65MO 286K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 118
#------------
#drive tc1 288
#drive tc2 288
#samplename "NS49MO RT"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 262
#------------
#drive tc1 300
#drive tc2 300
#samplename "NS49MO 300K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 262
#------------
#drive tc1 350
#drive tc2 350
#samplename "NS49MO 350K"
#runscan stth 4 5.2 25 time 46
#runscan stth 4 5.2 25 time 10
#runscan stth 4 5.2 25 time 262
#------------