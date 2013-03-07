drive msd 2500
drive sc 0
emon unregister tc1
broadcast "emon behaves!"
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
sampletitle ""
tc1 tolerance 10
#------------------
user "XXX"
title "P1622"

samplename XXX

#set j 200
#tc1 PowerLimit [expr $j/12]
#runscan stth 4.0 5.2 25 time 305
#runscan stth 4.0 5.2 25 time 305
#------------------

for {set i 250} {$i <= 500} {incr i 50} {
tc1 PowerLimit [expr $i/12]
drive tc1 [expr $i]
wait 900
samplename [concat XXX, $i C ]
runscan stth 4.0 5.2 25 time 118
}
