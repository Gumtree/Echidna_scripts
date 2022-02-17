# Collect a series of temperatures
# in the top loader

proc runtemps_up { templist timelist } {
	foreach kel_temperature $templist exptime $timelist {
		samplename [ concat HFWO, $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $exptime
	}
}

samplename HFWO at base
runscan stth 2.75 5.2 50 time 203
runtemps_up [list 7 7.5 8 8.5 9 10 16 16.5 17 17.5 18 19 ] [list 203 203 203 203 203 203 203 203 203 203 203 203] 
