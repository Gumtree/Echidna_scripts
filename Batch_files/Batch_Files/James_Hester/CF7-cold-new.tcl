# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist } {
	foreach kel_temperature $templist {
		samplename [ concat CTO, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		# hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 200
	}
}

# Make cold

#drive tc1_driveable 4

runtemps_up [list 20 35 75 140 150 225 275 ]

