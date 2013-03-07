drive msd 2500
drive sc 0
sampledescription "mtth120-noPC-noSC-331"
sampletitle "Proposal 681"
#drive pcx 135
#---------------
samplename "Ba18Sr02TiSi208"
user "Patryck Allen"
title "Test run for exposure determination"
robby send SampToVac(B,11,1)
wait 60
runscan stth 4.0 5.2 25 time 262
robby send VacRtn(B,11,1)
wait 60
