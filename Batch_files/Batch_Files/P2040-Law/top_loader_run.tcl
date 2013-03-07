# Collect a series of temperatures
# in the Orange cryostat
# The first temperature is ready
samplename CrPO4 (L62), 30K
runscan stth 4.0 5.2 25 time 550
#
proc runtemps_down1 {} {
	set templist [list 23 22 ]
	foreach kel_temperature $templist {
		samplename [ concat CrPO4 (L62), $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 600
		runscan stth 4.0 5.2 25 time 550
	}
}

runtemps_down1

hset /sample/tc1/control/pid_loop_1 150.0,20.0,5

proc runtemps_down2 {} {
	set templist [list 17 16]
	foreach kel_temperature $templist {
		samplename [ concat CrPO4 (L62), $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 600
		runscan stth 4.0 5.2 25 time 550
	}
}

runtemps_down2