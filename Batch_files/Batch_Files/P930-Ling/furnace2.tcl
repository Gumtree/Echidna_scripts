drive msd 2500
drive sc 0
emon unregister tc1
broadcast "emon behaves!"
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge331"
sampletitle "Ba4Sb2O9 heating run"
tc1 tolerance 5
tc1 RampRate 2000
#------------------
user "Matthew Dunstan"
title "P1373"

for {set i 500} {$i <= 1000} {incr i 50} {
tc1 PowerLimit [expr $i/16]
drive tc1 [expr $i]
wait 300
samplename [concat Ba4Sb2O9, $i C ]
runscan stth 4.0 5.2 25 time 95
}