# Collect a series of temperatures
# in the top loader

proc runtemps_up {} {
	set templist [list 4 350 ]
	foreach kel_temperature $templist {
		samplename [ concat SrCoO2.5, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		hset /sample/tc2/sensor/setpoint1 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 419
	}
}

samplename SrCoO3 at base in CF7
runscan stth 2.75 5.2 50 time 275

runtemps_up
