sampledescription "mtth140-noPC-noSC-OC1-Ge331"
title "P2617"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 60]
	foreach kel_temperature $templist {
		samplename [ concat Cu5V2O10, $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 900
		runscan stth 1.5 5.2 75 time 742
	}
}

# Start at 27K
samplename Cu5V2O10 at 27K
runscan stth 1.5 5.2 75 time 742
runtemps_up