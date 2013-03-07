drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-VacCh-Ge335"
title "DDT"

config rights manager ansto

#--------------
user "AONSA School"
robby send SampToVac(B,46,1)
wait 30
samplename "Mystery mixture - Raw"
runscan stth 4 5.2 25 time 694
robby send VacRtn(B,46,1)
wait 30
#--------------
robby send SampToVac(B,36,1)
wait 30
samplename "Mystery mixture - Ground"
runscan stth 4 5.2 25 time 694
robby send VacRtn(B,36,1)
wait 30
#--------------

robby send SampToVac(B,42,1)
wait 30
samplename "TiO2-aanatase"
runscan stth 4 5.2 25 time 694
robby send VacRtn(B,42,1)
wait 30

config rights user sydney
