# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat FePO4, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 275
	}
}

samplename FePO4 at 4K
runscan stth 2.75 5.2 50 time 275
runtemps_up [list 8 11 14 16 18 20 22 24 27 ]
