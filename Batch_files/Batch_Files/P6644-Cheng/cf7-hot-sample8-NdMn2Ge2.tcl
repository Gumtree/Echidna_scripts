# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat  NdMn2Ge2 $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 60
	}
}

runtemps_up [list 300 375 450 ]
# Now cool down
hset /sample/tc1/sensor/setpoint2 300
hset /sample/tc1/sensor/setpoint2 300
hset /sample/tc2/sensor/setpoint1 300
