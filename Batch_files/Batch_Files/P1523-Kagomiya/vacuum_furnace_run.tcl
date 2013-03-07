# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
title "Proposal 1523"
tc1 tolerance 2
tc1 ramprate 1000
#----
user Isao Kagomiya
title "Proposal 1523"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 300 600 800 850 ]
	foreach cel_temperature $templist {
		samplename [ concat Sr3FeCoO7-delta $cel_temperature C during heating]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 4.0 5.2 25 time 550
	}
}
runtemps_up