#--- List of temperatures
proc runtemps_up {} {
	set templist [list 450 550 650]
	foreach kel_temperature $templist {
		samplename [ concat SrCoO2.5, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 600
		runscan stth 2.75 5.2 50 time 419
	}
}

runtemps_up

hset /sample/tc1/sensor/setpoint2 2
hset /sample/tc2/sensor/setpoint1 2
hset /sample/tc1/sensor/setpoint1 2