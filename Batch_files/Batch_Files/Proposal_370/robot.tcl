user "Chris Ling, Catel Sebastien, Papegay Alexandre"
drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-Ge331-VC"
title "Proposal 370"
# allow sending robby commands
config rights manager ansto
    
samplename "LT-Ba4Nb08Ta12O9"
#robby send SampToVac(B,12,1)
#wait 60
runscan stth 2.75 5.2 50 time 118 
robby send VacRtn(B,12,1)
wait 60

samplename "LT-Ba4Nb04Ta16O9"
robby send SampToVac(B,13,1)
wait 60
runscan stth 2.75 5.2 50 time 118 
robby send VacRtn(B,13,1)
wait 60

samplename "Cu2NiB2O6"
robby send SampToVac(B,14,1)
wait 60
runscan stth 2.75 5.2 50 time 190 
robby send VacRtn(B,14,1)
wait 60

sampledescription "mtth140-noPC-noSC-Ge335-VC"
drive mom 69.98

samplename "Ba3BiIr2O9"
robby send SampToVac(B,15,1)
wait 60
runscan stth 2.75 5.2 50 time 478 
robby send VacRtn(B,15,1)
wait 60

samplename "Ba3LaIr2O9"
robby send SampToVac(B,16,1)
wait 60
runscan stth 2.75 5.2 50 time 262 
runscan stth 2.75 5.2 50 time 46 
runscan stth 2.75 5.2 50 time 46 
runscan stth 2.75 5.2 50 time 46 
runscan stth 2.75 5.2 50 time 46 
robby send VacRtn(B,16,1)
wait 60


config rights user sydney