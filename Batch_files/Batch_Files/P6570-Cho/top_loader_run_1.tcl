# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat LuInFeO3, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 635
	}
}

samplename LuInFeO3_10K
runscan stth 2.75 5.2 50 time 655
runtemps_up [list 50 200 250 ]
