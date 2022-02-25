# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat Bi08La02FeO3-43PbTiO3 $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 131
	}
}

samplename Bi08La02FeO3-43PbTiO3 at base
runscan stth 2.75 5.2 50 time 131
runtemps_up [list 150 300 ]
