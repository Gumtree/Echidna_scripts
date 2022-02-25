# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist } {
	foreach kel_temperature $templist {
		samplename [ concat Mn4Ta2O9, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		# hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 491
	}
}

samplename Mn4Ta4O9 at 120K
runscan stth 2.75 5.2 50 time 491
runtemps_up [list 150 250 ] 
