# Collect a series of temperatures
# in the top loader

proc runtemps_up {} {
	set templist [list 4]
	foreach kel_temperature $templist {
		samplename [ concat SrCoO3, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		hset /sample/tc2/sensor/setpoint1 $kel_temperature
		drive tc1_driveable $kel_temperature
		runscan stth 2.75 5.2 50 time 285
	}
}

samplename SrCoO3, 350K
hset /sample/tc1/sensor/setpoint2 350
hset /sample/tc2/sensor/setpoint1 300
drive tc1_driveable 350
runscan stth 2.75 5.2 50 time 118

hset /sample/tc1/sensor/setpoint2 300
hset /sample/tc1/sensor/setpoint1 300