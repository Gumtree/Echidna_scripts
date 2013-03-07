drive msd 2500
drive sc 0
emon unregister tc1
broadcast "emon behaves!"
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge331"
sampletitle "A-Ba4Nb0.4Ta1.6O9 heating run"
tc1 tolerance 5
tc1 RampRate 2000
#------------------
user "Matthew Dunstan"
title "P1373"

for {set i 1000} {$i <= 1450} {incr i 25} {
tc1 PowerLimit [expr $i/16]
drive tc1 [expr $i]
wait 300
samplename [concat A-Ba4Ta2O9, $i C ]
runscan stth 4.0 5.2 25 time 95
}