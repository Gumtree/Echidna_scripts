# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat TbCr0.95Mn0.05O3, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 347
	}
}

runtemps_up [list 5 70 200 300 ]
