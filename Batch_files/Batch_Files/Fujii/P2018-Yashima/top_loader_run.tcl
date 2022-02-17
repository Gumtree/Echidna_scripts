# Collect a series of temperatures
# in the top loader
hset /sample/tc1/sensor/setpoint2 5
drive tc1_driveable 5
wait 300
runscan stth 4.0 5.2 25 time 449
#
proc runtemps_up {} {
	set templist [list 50 90 150 200 250]
	foreach kel_temperature $templist {
		samplename [ concat Li doped silver niobate, $kel_temperature K ]
		# convert to Celcius for furnace driver
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 4.0 5.2 25 time 132
	}
}

runtemps_up