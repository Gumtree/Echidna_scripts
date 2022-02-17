# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat  Mg2.1FeSn0.9 $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 131
	}
}

runtemps_up [list 350 ]
# Now cool down
hset /sample/tc1/sensor/setpoint2 4
hset /sample/tc1/sensor/setpoint2 4
hset /sample/tc2/sensor/setpoint1 4
