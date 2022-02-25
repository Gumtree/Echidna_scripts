# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat Iron oxide mixture 7, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc2/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 131
	}
}

hset /sample/tc1/sensor/setpoint2 10
hset /sample/tc2/sensor/setpoint1 3
hset /sample/tc1/heater/heaterRange_1 5
hset /sample/tc1/heater/heaterRange_2 5
hset /sample/tc2/heater/heaterRange_1 5
#drive tc1_driveable 10
runtemps_up [list 50 80 110 140 170 200 230 260  ]
