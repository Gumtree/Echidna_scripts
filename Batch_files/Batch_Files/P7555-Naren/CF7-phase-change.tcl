# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist } {
	foreach kel_temperature $templist {
		samplename [ concat CrTaO, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 1200
		runscan stth 2.75 5.2 50 time 131
	}
}

#samplename CrTaO at base
#runscan stth 2.75 5.2 50 time 131
hset /sample/tc1/sensor/setpoint1 150
#
drive tc2_driveable 150
runtemps_up [list 175 200 225 ] 
