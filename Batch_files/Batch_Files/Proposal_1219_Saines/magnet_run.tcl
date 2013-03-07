title Proposal 1404
sampledescription mtth120-noPC-noSC-Ge331-magnet
user Paul Saines
drive sc 0
drive msd 2500
proc runmag_up {} {
	set maglist [list 2.45 3.5]
	foreach field $maglist {
		magnet send s $field
		wait 300
samplename [concat Mn Succinate at 2K, $field T]
runscan stth 2.75 5.2 50 time 262
	}
}
#proc runmag_up_again {} {
#	set maglist [list 2.0 3.0 4.0]
#	foreach field $maglist {
#		magnet send s $field
#		wait 30
#		magnet send s $field
#		wait 30
#		magnet send s $field
#		wait 300
#samplename [concat Mn Succinate at 8K, $field T]
#runscan stth 2.75 5.2 50 time 262
#	}
#}

# Actual executed lines
runmag_up
magnet send s 0
wait 300
drive tc1_driveable 8.0
runmag_up_again