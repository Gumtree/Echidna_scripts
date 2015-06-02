#--- List of temperatures
proc runtemps_down {} {
	set templist [list 350 340 330 ]
	foreach kel_temperature $templist {
		samplename [ concat SrCoO3, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 600
		runscan stth 2.75 5.2 50 time 203
	}
}



hset /sample/tc1/sensor/setpoint2 250
hset /sample/tc1/sensor/setpoint1 250
hset /sample/tc2/sensor/setpoint1 250

drive tc1_driveable 250

samplename SrCoO3 at 250K

runscan stth 2.75 5.2 50 time 160

hset /sample/tc1/sensor/setpoint2 300
hset /sample/tc1/sensor/setpoint1 300
hset /sample/tc2/sensor/setpoint1 300

drive tc1_driveable 220

samplename SrCoO3 at 220K

runscan stth 2.75 5.2 50 time 160

