sampledescription "mtth140-noPC-noSC-OC1-Ge331"
title "Proposal 2581"
#--- List of temperatures
proc runtemps_up {}{
	
	samplename [ concat LiCuO, 15 K ]
	drive tc1_driveable 15
	wait 60
	runscan stth 2.75 5.2 50 time 419
	
	samplename [ concat LiCuO, 30 K ]
	drive tc1_driveable 30
	wait 600
	runscan stth 2.75 5.2 50 time 419
	
	samplename [ concat LiCuO, 200 K ]
	drive tc1_driveable 200
	wait 900
	runscan stth 2.75 5.2 50 time 59
	
	samplename [ concat LiCuO, 300 K ]
	drive tc1_driveable 300
	wait 900
	runscan stth 2.75 5.2 50 time 59
	

	
}

runtemps_up