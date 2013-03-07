user "John Bradley"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-335"
title "Proposal 577"
# allow sending robby commands
config rights manager ansto
#===========================
drive mchi -0.12
#===========================    
samplename "Nd10"
robby send SampToVac(B,32,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,32,1)
wait 60
#==================================
drive mchi -0.05
#==================================
samplename "La10"
robby send SampToVac(B,33,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,33,1)
wait 60
#==================================
samplename "La11"
robby send SampToVac(B,34,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,34,1)
wait 60
#==================================
samplename "Al2O3-small"
robby send SampToVac(B,2,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,2,1)
wait 60
#==================================
samplename "La12 test"
robby send SampToVac(B,36,1)
wait 60
runscan stth 4.0 5.2 25 time 262
robby send VacRtn(B,36,1)
#===================================
config rights user sydney