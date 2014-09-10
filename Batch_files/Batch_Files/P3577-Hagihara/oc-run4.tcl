# Collect a series of temperatures
# in the orange cryostat


samplename CaCo(VO4)OD at 12K
runscan stth 2.75 5.2 50 time 59



proc runtemps_up templist {
	foreach kel_temperature $templist {
		samplename [ concat CaCo(VO4)OD, $kel_temperature K ]
		drive tc1_driveable $kel_temperature
		wait 300
		runscan stth 2.75 5.2 50 time 59
	}
}

set templist [list 12.5 13]
runtemps_up $templist
