# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast "emon behaves!"
#
sampledescription "mtth140-noPC-noSC-VacFurnace-Ge335"
title "Proposal 1324"
tc1 tolerance 10
tc1 ramprate 500
#----
user Jian-Li Wang
title "Proposal 1324"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 550 575 600 650 700 750 750]
	foreach kel_temperature $templist {
		samplename [ concat Mn50Ni25Co10Ga15 ribbon, $kel_temperature K during heating]
		# convert to Celcius for furnace driver
		set cel_temperature [expr $kel_temperature - 273]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 4.0 5.2 25 time 118
	}
}

proc runtemps_down {} {
	set templist [list 650 575 550 525 500 450 350 ]
	foreach kel_temperature $templist {
		samplename [ concat Mn50Ni25Co10Ga15 ribbon, $kel_temperature K during cooling]
		# convert to Celcius for furnace driver
		set cel_temperature [expr $kel_temperature - 273]
		# adjust West 400 max power to improve stability
		tc1 PowerLimit [expr $cel_temperature/15]
		drive tc1 $cel_temperature
		wait 300
		runscan stth 4.0 5.2 25 time 118
	}
}
runtemps_up
# now cool down
runtemps_down