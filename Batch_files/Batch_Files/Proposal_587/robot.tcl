user "Brendan Kennedy"
drive msd 2500
drive sc 1
sampledescription "mtth140-noPC-SC10-337"
title "Proposal 587"
# allow sending robby commands
config rights manager ansto    
samplename "Sr0.85Nd0.15MnO3"
robby send SampToVac(B,31,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,31,1)
wait 60
#===============================
samplename "Sr0.825Nd0.175MnO3"
robby send SampToVac(B,32,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,32,1)
wait 60
#===============================
samplename "Sr0.8Nd0.20MnO3"
robby send SampToVac(B,33,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,33,1)
wait 60
#===============================
samplename "Sr0.775Nd0.225MnO3"
robby send SampToVac(B,34,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,34,1)
wait 60
#===============================
samplename "Sr0.75Nd0.25MnO3"
robby send SampToVac(B,35,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,35,1)
wait 60
#===============================
samplename "Corundum wavelength standard"
robby send SampToVac(B,01,1)
wait 60
runscan stth 4.0 5.2 25 time 118
robby send VacRtn(B,01,1)
wait 60
#===============================
config rights user sydney