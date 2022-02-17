# Running in orange cryostat

proc runtemps_up { templist timelist } {
	foreach kel_temperature $templist exp_time $timelist {
		samplename [ concat EFWO_ $kel_temperature K ]
		# set cold head temperature
		drive tc1_temp6_setpoint $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exp_time
	}
}

runtemps_up [list 7.5 12.5 14 40 ] [list 275 275 131 131 ]

