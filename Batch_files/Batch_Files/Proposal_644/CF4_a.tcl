drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-CF1-Ge335"
sampletitle "FeSe0.3Te0.7"
user "Tzu-Wen Huang, Kuo-Wei Yeh"
title "Proposal 644"
tc1 range 5
tc1 controlsensor sensorB
tc1 tolerance 500
tc1 heateron 0
#-------------
#samplename "(FeSe0.3Te0.7) cooling down"
#runscan stth 4 5.2 25 time 46
samplename "(FeSe0.3Te0.7) base T(2K)"
runscan stth 4 5.2 25 time 550
runscan stth 4 5.2 25 time 550
runscan stth 4 5.2 25 time 550
#-------------
tc1 heateron 1
#-------------
drive tc1 50
samplename "(FeSe0.3Te0.7) going to 50K"
runscan stth 4 5.2 25 time 46
samplename "(FeSe0.3Te0.7) 50K"
runscan stth 4 5.2 25 time 550
runscan stth 4 5.2 25 time 550
runscan stth 4 5.2 25 time 550
#-------------
drive tc1 150
samplename "(FeSe0.3Te0.7) going to 150K"
runscan stth 4 5.2 25 time 46
samplename "(FeSe0.3Te0.7) 150K"
runscan stth 4 5.2 25 time 550
runscan stth 4 5.2 25 time 550
runscan stth 4 5.2 25 time 550
drive tc1 300