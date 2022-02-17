# Collect a series of temperatures
# in the top loader

proc runtemps_up {templist timelist} {
	foreach kel_temperature $templist exp_time $timelist {
		samplename [ concat Mg2.1FeSn0.9 $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exp_time
	}
}

samplename Mg2.1FeSn0.9 at base
runscan stth 2.75 5.2 50 time 203
runtemps_up [list 50 100 150 200 225 250 275 300 ] [list 131 131 131 131 203 131 131 203 ]
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4
hset /sample/tc2/sensor/setpoint1 4