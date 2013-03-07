sampledescription "mtth140-noPC-noSC-CF7-Ge335"
title "Proposal 2309"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 313 343 373 403]
	foreach kel_temperature $templist {
		samplename [ concat LSTMN1_Li, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 600
		runscan stth 2.75 5.2 50 time 275
	}
}

samplename LSTMN1_Li at 296K in CF7, 1hr
runscan stth 2.75 5.2 50 time 60
runtemps_up