# Running in orange cryostat

proc runtemps_up { templist } {
	foreach kel_temperature $templist {
		samplename [ concat FTO_ $kel_temperature K ]
		# set cold head temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 203
	}
}

runtemps_up [list 5 7.5 15 25 40 45 52.5 60 65 75 85 ]