# Collect a series of temperatures
# in the top loader

set smpname [SplitReply [samplename]]

proc runtemps_up { templist timelist smpname } {
	foreach kel_temperature $templist scan_time $timelist {
		samplename [ concat $smpname $kel_temperature K ]
		# set cold head temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time $scan_time
	}
}

#get to base
#hset /sample/tc2/sensor/setpoint1 4
#drive tc1_driveable 5
#samplename [concat $smpname at base]
runscan stth 2.75 5.2 50 time 131
runtemps_up [list 110 120 ] [list 131 131 ] $smpname
