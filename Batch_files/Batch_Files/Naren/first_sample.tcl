set spname [lindex [hval /sample/name] 0]

set mylist [list 25.0 50.0 75.0 110.0 125.0 ]

proc hightemps {temperlist spname} {
	foreach temper $temperlist {
		samplename [concat $spname at $temper K]
		drive tc1_driveable $temper
		wait 600
		runscan stth 2.75 5.2 50 time 131
	}
}

samplename [concat $spname at base]

drive tc1_driveable 10
hset /sample/pc1/setpoint 5
drive tc1_driveable 1
wait 300

runscan stth 2.75 5.2 50 time 131

hightemps $mylist $spname

