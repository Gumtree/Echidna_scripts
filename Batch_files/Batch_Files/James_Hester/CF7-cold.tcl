# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist timelist } {
	foreach kel_temperature $templist exptime $timelist {
		samplename [ concat CoTaO, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exptime
	}
}

samplename CoTaO at base
runscan stth 2.75 5.2 50 time 707
runtemps_up [list 9 11 16 18 20 25 ] [list 60 60 60 60 60 707 ] 
