drive msd 2500
drive sc 0
sampledescription "mtth140-npPC-noSC-CF1-Ge331"
sampletitle "BaCuB2O5"
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
samplename "BaCuB2O5 going to 150K"
runscan stth 4 5.2 25 time 118
samplename "BaCuB2O5 150K"
runscan stth 4 5.2 25 time 550
#-------------
#drive tc1 370
#drive tc2 370
#samplename "BaCuB2O5 base T"
#runscan stth 4 5.2 25 time 118
#runscan stth 4 5.2 25 time 262
#-------------
