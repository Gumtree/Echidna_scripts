# Collect a series of temperatures
# in the top loader

proc runtemps_up {templist timelist} {
	foreach kel_temperature $templist exp_time $timelist {
		samplename [ concat Ho2Fe15Mn2 $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exp_time
	}
}

samplename Ho2Fe15Mn2 at base
runscan stth 2.75 5.2 50 time 131
runtemps_up [list 100 ] [list 131]
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4
hset /sample/tc2/sensor/setpoint1 4