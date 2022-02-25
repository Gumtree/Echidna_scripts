# Collect a series of temperatures
# in the top loader

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat dHMB, $kel_temperature K ]
		# set vti temperature
		drive tc1_temp0_setpoint $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 131
	}
}

runtemps_up [list 1.7 35 42 50 125 130 140 ]
