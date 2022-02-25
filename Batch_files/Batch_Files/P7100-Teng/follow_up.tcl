
set smpname [SplitReply [samplename]]

proc runtemps_up { templist smpname } {
	foreach kel_temperature $templist {
		samplename [ concat $smpname $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		drive tc1_driveable2 $kel_temperature
		wait 600
		runscan stth 2.75 5.2 50 time 275
	}
}

samplename $smpname at 300K
runscan stth 2.75 5.2 50 time 275
#
runtemps_up [list 350 ] $smpname