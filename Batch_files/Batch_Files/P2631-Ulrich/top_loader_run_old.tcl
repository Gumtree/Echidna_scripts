# Collect a series of temperatures
# in the top loader

proc runtemps_up {} {
	set templist [list 13 25 60 ]
	foreach kel_temperature $templist {
		samplename [ concat DyMnO3, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 1.5 5.2 75 time 1078
	}
}

runtemps_up
