# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat Na2Mn3O7, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 275
	}
}

# one hour cooling
runscan stth 2.75 5.2 50 time 60
# now automatically get to base
drive tc2_driveable 4
# and wait for the other bits as well
drive tc1_driveable 6
# and set back to four
hset /sample/tc1/sensor/setpoint1 4
wait 300
samplename Na2Mn3O7 at base
runscan stth 2.75 5.2 50 time 300
runtemps_up [list 12 45 ]
