drive msd 2500
drive sc 0
sampledescription "mtth140-noPC-noSC-VacCh-Ge331"
sampletitle ""
title "DDT"
#---------------
config rights manager ansto
#--------------
user "eileen"
#robby send SampToVac(A,1,1)
#wait 60
samplename "Ag-0"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,1,1)
wait 60
#--------------
user "eileen"
robby send SampToVac(A,2,1)
wait 60
samplename "Ag-1"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,2,1)
wait 60
#--------------
user "eileen"
robby send SampToVac(A,3,1)
wait 60
samplename "Ag-2"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,3,1)
wait 60
#--------------
user "eileen"
robby send SampToVac(A,4,1)
wait 60
samplename "Ag-3"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,4,1)
wait 60
#--------------
user "eileen"
robby send SampToVac(A,5,1)
wait 60
samplename "Ag-4"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,5,1)
wait 60
#--------------
user "eileen"
robby send SampToVac(A,6,1)
wait 60
samplename "Ag-5"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,6,1)
wait 60
#--------------
user "eileen"
robby send SampToVac(A,7,1)
wait 60
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,7,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,11,1)
wait 60
samplename "Cl-0"
runscan stth 1.5 5.2 75 time 118
robby send VacRtn(A,11,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,12,1)
wait 60
samplename "Co-1"
runscan stth 1.5 5.2 75 time 118
robby send VacRtn(A,12,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,13,1)
wait 60
samplename "Co-2"
runscan stth 1.5 5.2 75 time 118
robby send VacRtn(A,13,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,14,1)
wait 60
samplename "Fe-1"
runscan stth 1.5 5.2 75 time 118
robby send VacRtn(A,14,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,15,1)
wait 60
samplename "Fe-2"
runscan stth 1.5 5.2 75 time 118
robby send VacRtn(A,15,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,21,1)
wait 60
samplename "Zn-1"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,21,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,22,1)
wait 60
samplename "Zn-2"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,22,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,23,1)
wait 60
samplename "Zn-3"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,23,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,24,1)
wait 60
samplename "Zn-4"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,24,1)
wait 60
#--------------
user "Houran"
robby send SampToVac(A,25,1)
wait 60
samplename "Zn-5"
runscan stth 1.5 5.2 75 time 262
robby send VacRtn(A,25,1)
wait 60

config rights user sydney
