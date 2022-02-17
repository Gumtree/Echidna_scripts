# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
title "Proposal 1868"
tc1 tolerance 3
tc1 ramprate  5
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 45 70 100 150 30 ]
	foreach cel_temperature $templist {
		samplename [ concat LST10_018_Li, $cel_temperature C ]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 1.5 5.2 75 time 118
	}
}

# room temperature first
samplename LST10_018_Li
runscan stth 1.5 5.2 75 time 118
# now the other temperatures
runtemps_up
# now cool down
tc1 ramprate 10000
drive tc1 0