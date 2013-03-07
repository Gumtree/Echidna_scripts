drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-Ge331-OC"
sampletitle "Ammonium borodeuteride"
user "Mark Bowden"
samplename "Ammonium borodeuteride"
title "Proposal 628"
tc2 range 5       
tc2 controlsensor sensorA
tc2 tolerance 100
tc2 heateron 1
#-------------
drive tc2 60
runscan stth 4 5.2 25 time 118
runscan stth 1.5 5.2 75 time 70
drive tc2 55
wait 600
runscan stth 1.5 5.2 75 time 70
drive tc2 50
wait 600
runscan stth 1.5 5.2 75 time 70
drive tc2 45
wait 600
runscan stth 1.5 5.2 75 time 70
drive tc2 40
wait 600
runscan stth 1.5 5.2 75 time 70
drive tc2 35
wait 600
runscan stth 1.5 5.2 75 time 70
