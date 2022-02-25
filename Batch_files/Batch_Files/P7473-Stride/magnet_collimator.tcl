# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat dHMB, $kel_temperature K, collimator ]
		# set vti temperature
		drive tc1_temp0_setpoint $kel_temperature
		wait 900
		runscan stth 2.75 5.2 50 time 203
	}
}

samplename dHMB with collimator zero field base temperature
runscan stth 2.75 5.2 50 time 203

runtemps_up [list 20 40 50 60 80 100 125 130 140 160 180 ]
