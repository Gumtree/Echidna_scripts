drive msd 2500
drive sc 0
sampledescription "mtth140-npPC-noSC-CF1-Ge335"
sampletitle "(FeMn)(SeTe)"
user "Tzu-Wen Huang, Kuo-Wei Yeh"
title "Proposal 644"
tc1 range 5
tc1 controlsensor sensorB
tc1 tolerance 500
tc1 heateron 0
#-------------
#samplename "(FeMn)(SeTe) cooling down"
#runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) base T"
runscan stth 4 5.2 25 time 406
#-------------
tc1 heateron 1
#-------------
drive tc1 10
samplename "(FeMn)(SeTe) going to 10K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 10K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 15
samplename "(FeMn)(SeTe) going to 15K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 15K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 20
samplename "(FeMn)(SeTe) going to 20K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 20K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 50
samplename "(FeMn)(SeTe) going to 50K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 50K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 75
samplename "(FeMn)(SeTe) going to 75K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 75K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 100
samplename "(FeMn)(SeTe) going to 100K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 100K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 125
samplename "(FeMn)(SeTe) going to 125K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 125K"
runscan stth 4 5.2 25 time 406
#-------------
drive tc1 150
samplename "(FeMn)(SeTe) going to 150K"
runscan stth 4 5.2 25 time 46
samplename "(FeMn)(SeTe) 150K"
runscan stth 4 5.2 25 time 406
drive tc1 300
