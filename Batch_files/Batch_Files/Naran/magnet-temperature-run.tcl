# Collect a series of temperatures
# in the top loader

proc runtemps_up {} {
	set templist [list 25 50 ]
	foreach kel_temperature $templist {
		samplename [ concat Pb3MnO15, $kel_temperature K ]
		hset /sample/tc1/Loop1/setpoint $kel_temperature
		wait 600
		runscan stth 2.75 5.2 50 time 419
	}
}

samplename Pb3MnO15 at 5K
runscan stth 2.75 5.2 50 time 419
runtemps_up
