# Run CF7 above RT
proc runtemps_up_hot templist {
	foreach kel_temperature $templist {
		samplename [ concat Co2CrAl, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc1_driveable2 $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 419
	}
}

hset /sample/tc2/sensor/setpoint1 300
runtemps_up_hot [list 400]
# Go to next temperature
hset /sample/tc1/sensor/setpoint1 100
hset /sample/tc1/sensor/setpoint2 100
drive tc2_driveable 100
