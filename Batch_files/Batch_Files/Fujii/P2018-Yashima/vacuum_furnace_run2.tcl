# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
title "Proposal 2018"
tc1 tolerance 5
tc1 ramprate 1000
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 200 400 600 800 1000]
	foreach cel_temperature $templist {
		samplename [ concat CaYAlO4, $cel_temperature C ]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 4.0 5.2 25 time 65
	}
}

runtemps_up
samplename CaYAlO4 at 1200C
tc1 PowerLimit [expr 1200/15]
drive tc1 1200
wait 300
runscan stth 4.0 5.2 25 time 382
# now cool down
tc1 ramprate 10000
drive tc1 0