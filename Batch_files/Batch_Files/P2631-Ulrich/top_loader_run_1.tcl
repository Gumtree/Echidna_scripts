# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat Cu0.7Fe2.3O4, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 1200
		runscan stth 2.75 5.2 50 time 203
	}
}

#get to base
#hset /sample/tc2/sensor/setpoint1 4
#drive tc1_driveable 7
runtemps_up [list 5 200 ]
