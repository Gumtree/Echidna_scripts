# Collect a series of temperatures
# in the orange cryostat


samplename CaCo(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 118

samplename CaCo(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 118

proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat CaCo(VO4)OD, $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 118
	}
}

set templist [list 3.5 5.5 7.5 9.5 10.5 11.5 13.5 15.5]
runtemps_up $templist
