user "John Bradley"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-335"
title "Proposal 577"
# allow sending robby commands
config rights manager ansto    
samplename "Y5La5W2O21"
robby send SampToVac(B,31,1)
wait 60
runscan stth 4.0 5.2 25 time 1414
robby send VacRtn(B,31,1)
wait 60
#==================================
samplename "La6W2O21"
robby send SampToVac(B,32,1)
wait 60
runscan stth 4.0 5.2 25 time 118
robby send VacRtn(B,32,1)
wait 60
#==================================
samplename "La10W2O21"
robby send SampToVac(B,33,1)
wait 60
runscan stth 4.0 5.2 25 time 118
robby send VacRtn(B,33,1)
wait 60
#==================================
samplename "La11W2O21"
robby send SampToVac(B,34,1)
wait 60
runscan stth 4.0 5.2 25 time 118
robby send VacRtn(B,34,1)
wait 60
#==================================
samplename "Y7.5La2.5W2O21"
robby send SampToVac(B,35,1)
wait 60
runscan stth 4.0 5.2 25 time 118
robby send VacRtn(B,35,1)
wait 60
#==================================
config rights user sydney