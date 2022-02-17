# Collect a series of temperatures
# in the top loader

set smpname [SplitReply [samplename]]

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat $smpname _ $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc2_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 311
	}
}

#get to base
#hset /sample/tc2/sensor/setpoint1 4
#drive tc1_driveable 5
samplename [concat $smpname _ base]
runscan stth 2.75 5.2 50 time 311
runtemps_up [list 110 120 200 ]
