# an overnight run
proc runtemps_up {} {
set templist [list 35 40 60 ]
foreach one_temp $templist {
	samplename [ concat HS37 at $one_temp K]
        drive tc1_driveable $one_temp
	wait 600
        runscan stth 2.75 5.2 50 time 419
}
}

runtemps_up