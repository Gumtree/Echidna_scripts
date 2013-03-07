# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
title "Proposal 2018"
tc1 tolerance 5
tc1 ramprate 1000
samplename PrSrBaCo2O5 x = 0.8 @ 28C

runscan stth 4.0 5.2 13 time 492
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 200 400 600 800]
	foreach cel_temperature $templist {
		samplename [ concat PrSrBaCo2O5 x=0.8, $cel_temperature C ]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 4.0 5.2 13 time 164
	}
}

runtemps_up
samplename PrSrBaCo2O5 x=0.8 at 1000C
tc1 PowerLimit [expr 1000/15]
drive tc1 1000
wait 300
runscan stth 4.0 5.2 13 time 492
# now cool down
tc1 ramprate 10000
drive tc1 0