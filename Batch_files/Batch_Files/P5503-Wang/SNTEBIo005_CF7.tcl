# Collect a series of temperatures
# in the top loader above room temperature

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat SnTeBIO02, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc1_driveable2 $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 59
	}
}

# switch on heaters
hset /sample/tc1/heater/heaterRange_1 5
hset /sample/tc1/heater/heaterRange_2 5
hset /sample/tc2/heater/heaterRange_1 5

hset /sample/tc2/sensor/setpoint1 300
runtemps_up [list 373 397 417 437 ]

hset /sample/tc1/control/tolerance2 10
samplename SnTeBIo005 at 700K
hset /sample/tc1/sensor/setpoint1 700
drive tc1_driveable2 700
wait 300
runscan stth 2.75 5.2 50 time 59

# cool down
hset /sample/tc1/control/tolerance2 1
hset /sample/tc1/sensor/setpoint1 323
drive tc1_driveable2 323
samplename SnTeBIo005 at 323K
wait 300
runscan stth 2.75 5.2 50 time 59
