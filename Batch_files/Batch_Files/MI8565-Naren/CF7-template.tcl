# Collect a series of temperatures
# in the top loader

set smpname [SplitReply [samplename]]

proc runtemps_up {templist sname} {
	foreach kel_temperature $templist {
		samplename [ concat $sname _ $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		# hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 203
	}
}

runtemps_up [list 90 92 95 97.5 100 115 ] $smpname
