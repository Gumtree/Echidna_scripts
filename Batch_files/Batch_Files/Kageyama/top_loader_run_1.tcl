# Collect a series of temperatures
# in the top loader

proc runtemps_up {} {
	set templist [list 300 ]
	foreach kel_temperature $templist {
		samplename [ concat No. 12 BTOD, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 59
	}
}

runtemps_up
