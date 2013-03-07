sampledescription "mtth140-noPC-noSC-OC1-Ge331"
title "Proposal 2581"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 30 10 20]
	foreach kel_temperature $templist {
		samplename [ concat LiCu1-xZnxO, $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 900
		runscan stth 2.75 5.2 50 time 563
	}
}

runtemps_up