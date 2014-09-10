# Collect a series of temperatures
# in the orange cryostat

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat CaCu(VO4)OD, $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 360
	}
}

samplename CaCu(VO4)OD at 10K
runscan stth 2.75 5.2 50 time 347
# now base temperature
drive tc1_driveable 1.5
wait 300
# now collect data
samplename CaCu(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 347
# now collect data
samplename CaCu(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 347
# now collect data
samplename CaCu(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 347
# ready to change sample
drive tc1_driveable 20
# now collect data
samplename CaCu(VO4)OD at 20K
runscan stth 2.75 5.2 50 time 95
#set templist [list 10 1.8]
#runtemps_up templist
