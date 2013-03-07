# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast emon behaves!
#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
tc1 tolerance 2
tc1 ramprate 1000
#----
user Siegbert Schmid
title Proposal 2309
#--- List of temperatures
proc runtemps_up {} {
set templist [list 427 577 827 577 327 ]
foreach cel_temperature $templist {
samplename [ concat LiMnTiO4-Q950 $cel_temperature C ]
# adjust West 400 max power to improve stability
tc1 PowerLimit [expr $cel_temperature/19]
drive tc1 $cel_temperature
wait 600
runscan stth 1.5 5.2 75 time 131
}
}

samplename LiMnTiO4-Q950 at RT (in Vac Furnace)
runscan stth 1.5 5.2 75 time 131
runtemps_up
