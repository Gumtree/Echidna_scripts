set spname [lindex [hval /sample/name] 0]

set mylist [list 110.0 ]

proc hightemps {temperlist spname} {
	foreach temper $temperlist {
		samplename [concat $spname at $temper K]
		drive tc1_driveable $temper
		wait 600
		runscan stth 2.75 5.2 50 time 262
	}
}

samplename [concat $spname at base2]

drive tc1_driveable 3
hset /sample/pc1/setpoint 2
drive tc1_driveable 1
wait 300

runscan stth 2.75 5.2 50 time 154

hightemps $mylist $spname

