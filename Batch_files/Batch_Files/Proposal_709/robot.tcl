user "Lasse Noren"
title "Proposal 709"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-335"
sampletitle "BaCuZnNbO solid solution"
# allow sending robby commands
config rights manager ansto    
samplename "709b (75)"
robby send SampToVac(B,34,1)
wait 60
runscan stth 4.0 5.2 25 time 406
robby send VacRtn(B,34,1)
wait 60
#========================
samplename "709c (50)"
robby send SampToVac(B,35,1)
wait 60
runscan stth 4.0 5.2 25 time 406
robby send VacRtn(B,35,1)
wait 60
#========================
samplename "709d (30)"
robby send SampToVac(B,36,1)
wait 60
runscan stth 4.0 5.2 25 time 406
robby send VacRtn(B,36,1)
wait 60
#========================
samplename "709e (25)"
robby send SampToVac(B,37,1)
wait 60
runscan stth 4.0 5.2 25 time 406
robby send VacRtn(B,37,1)
wait 60
#========================
samplename "709f (1)"
robby send SampToVac(B,38,1)
wait 60
runscan stth 4.0 5.2 25 time 406
robby send VacRtn(B,38,1)
wait 60
#========================
samplename "709pi (pi)"
robby send SampToVac(B,40,1)
wait 60
runscan stth 4.0 5.2 25 time 406
robby send VacRtn(B,40,1)
wait 60
#========================
config rights user sydney