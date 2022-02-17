# Collect a series of temperatures
# in the top loader

hset /sample/tc2/sensor/setpoint1 300

set smpname [SplitReply [samplename]]

proc runtemps_up { templist smpname } {
	foreach kel_temperature $templist {
		samplename [ concat $smpname $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc1_driveable2 $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 263
	}
}

samplename [concat $smpname at RT]
runscan stth 2.75 5.2 50 time 263
#
runtemps_up [list 380 445 600] $smpname