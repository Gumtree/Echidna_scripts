sampledescription "mtth140-noPC-noSC-OC1-Ge331"
title "Proposal 2581"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 15 15 30 30]
	foreach kel_temperature $templist {
		samplename [ concat LiCuO, $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 600
		runscan stth 2.75 5.2 50 time 203
	}
}

runtemps_up