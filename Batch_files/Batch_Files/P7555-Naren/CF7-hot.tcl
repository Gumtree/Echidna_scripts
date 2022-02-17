# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist } {
	foreach kel_temperature $templist {
		samplename [ concat CrTaO, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 1200
		runscan stth 2.75 5.2 50 time 131
	}
}

samplename CrTaO at 300K on ht stick
runscan stth 2.75 5.2 50 time 131
runtemps_up [list 350 400 450 500 550 600 650 ] 
