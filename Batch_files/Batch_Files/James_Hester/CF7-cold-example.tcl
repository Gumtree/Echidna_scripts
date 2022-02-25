# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist timelist } {
	foreach kel_temperature $templist exptime $timelist {
		samplename [ concat CTO $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exptime
	}
}


runtemps_up [list 100 200 300 ] [list 203 203 203 ] 
