# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat mysample, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc2/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 1.5 5.2 75 time 1078
	}
}

runtemps_up [list 10 20 30 ]
