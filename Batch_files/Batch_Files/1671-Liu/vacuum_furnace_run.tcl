# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
title "Proposal 1671"
tc1 tolerance 2
tc1 ramprate 600
#----
user Meinan Liu
title "Proposal 1671"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 200 400 450 475 500 525 550 575 600 650 700 ]
	foreach cel_temperature $templist {
		samplename [ concat NaNbO3-n type 2nd try $cel_temperature C during heating]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 1.5 5.2 75 time 262
	}
}
runtemps_up
drive tc1 0
