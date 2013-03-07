# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-SC10-VacFurnace-Ge335"
title "Proposal 2604"
tc1 tolerance 2
tc1 ramprate 1000
#----
user Siegbert Schmid
title "P2604"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 450 550 750 1100]
	foreach cel_temperature $templist {
		samplename [ concat SMN025 $cel_temperature C during heating]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/30]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 419
	}
}
runtemps_up