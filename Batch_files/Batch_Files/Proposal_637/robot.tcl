user "John Provis"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-331"
title "Proposal 637"
# allow sending robby commands
config rights manager ansto    
samplename "D750"
robby send SampToVac(B,41,1)
wait 60
runscan stth 4.0 5.2 25 time 550
robby send VacRtn(B,41,1)
wait 60
#===============================
config rights user sydney