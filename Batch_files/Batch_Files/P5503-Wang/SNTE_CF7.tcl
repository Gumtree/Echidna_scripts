# Collect a series of temperatures
# in the top loader above room temperature

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat SnTe, $kel_temperature K ]
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
runtemps_up [list  373 483 493 503 513 523 573 623 673 ]

# 2 hour run
hset /sample/tc1/control/tolerance2 10
hset /sample/tc1/sensor/setpoint1 700
drive tc1_driveable2 700
wait 600
samplename SnTe at 700K
runscan stth 2.75 5.2 50 time 131
# cool down
hset /sample/tc1/control/tolerance2 1
hset /sample/tc1/sensor/setpoint1 323
drive tc1_driveable2 323
samplename SnTe at 323K
wait 300
runscan stth 2.75 5.2 50 time 59
#
hset /sample/tc1/control/tolerance2 1
hset /sample/tc1/sensor/setpoint1 323
drive tc1_driveable2 323
samplename SnTe at 323K second time
wait 300
runscan stth 2.75 5.2 50 time 59