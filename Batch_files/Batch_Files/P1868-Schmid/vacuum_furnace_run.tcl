sampledescription "mtth140-noPC-noSC-CF7-Ge335"
title "Proposal 1868"
#--- List of temperatures
proc runtemps_up {} {
	set templist [list 295 338 343 373 423 ]
	foreach kel_temperature $templist {
		samplename [ concat LST10_018_Li, $kel_temperature K ]
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 1.5 5.2 75 time 118
	}
}

# 45C done by hand
samplename LST10_018_Li at 45C
runscan stth 1.5 5.2 75 time 118
# now the other temperatures
# 70C also done by hand
drive tc1 70
wait 300
samplename LST10_018_Li at 70C
runscan stth 1.5 5.2 75 time 118
runtemps_up
# now cool down
tc1 ramprate 10000
drive tc1 0