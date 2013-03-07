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
	set templist [list 200 400]
	foreach cel_temperature $templist {
		samplename [ concat YBaCo2.5Zn1.5O7, $cel_temperature C ]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 4.0 5.2 13 time 305
	}
}

runtemps_up
samplename YBaCo2.5Zn1.5O7 at 600C
tc1 PowerLimit [expr 600/15]
drive tc1 600
wait 300
runscan stth 4.0 5.2 13 time 915

samplename YBaCo2.5Zn1.5O7 at 800C
tc1 PowerLimit [expr 800/15]
drive tc1 800
wait 300
runscan stth 4.0 5.2 13 time 305

# now cool down
tc1 ramprate 10000
drive tc1 0