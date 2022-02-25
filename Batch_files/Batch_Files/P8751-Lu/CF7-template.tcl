# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat AgNb7O18 _ $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 255
	}
}

#get to base
#hset /sample/tc2/sensor/setpoint1 4
#drive tc1_driveable 5
samplename AgNb7O18_base
runscan stth 2.75 5.2 50 time 255
runtemps_up [list 100 200 300 ]
#
# do a high temperature as well

samplename AgNb7O18_450K
# set cold head temperature
hset /sample/tc1/sensor/setpoint1 450
hset /sample/tc1/sensor/setpoint2 450
drive tc1_driveable2 450
wait 300
runscan stth 2.75 5.2 50 time 255
