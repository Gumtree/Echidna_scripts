# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat Ca3Ti2O7_ $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 230
	}
}

runtemps_up [list 4 50 100 200 ]  

hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc2/sensor/setpoint1 4
