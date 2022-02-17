# Collect a series of temperatures
# in the top loader

proc runtemps_up {templist timelist} {
	foreach kel_temperature $templist exp_time $timelist {
		samplename [ concat LaMn2Ge2 $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exp_time
	}
}

samplename LaMn2Ge2 at base
runscan stth 2.75 5.2 50 time 131
runtemps_up [list 100 200 300 ] [list 131 131 131 ]
hset /sample/tc1/sensor/setpoint1 300
hset /sample/tc1/sensor/setpoint2 300
hset /sample/tc2/senshistmemor/setpoint1 300