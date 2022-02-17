# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist timelist } {
	foreach kel_temperature $templist exptime $timelist {
		samplename [ concat LuInFeO3 $kel_temperature K ]
		drive tc1_driveable $kel_temperature tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exptime
	}
}


runtemps_up [list 400 ] [list 203 ] 
