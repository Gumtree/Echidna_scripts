# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist } {
	foreach kel_temperature $templist {
		samplename [ concat MVO, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		# hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 455
	}
}

# Make cold

#drive tc1_driveable 4

samplename MVO at 21K
runscan stth 2.75 5.2 50 time 131

samplename MVO at 35K
hset /sample/tc1/sensor/setpoint1 35
drive tc2_driveable 35
wait 300
runscan stth 2.75 5.2 50 time 131

runtemps_up [list 70 250 ]

hset /sample/tc1/sensor/setpoint1 4
drive tc2_driveable 4

