# Collect a series of temperatures
# in the air furnace using invisible sics
# internal tree

proc runtemps_up {} {
	set templist [list 427 577 827 577 327]
	foreach cel_temperature $templist {
		samplename [ concat LMTQ in alumina holder in air furnace, $cel_temperature C ]
		hset /sics/tc1/setpoint $cel_temperature
		wait 1
		set curval [lindex [ split [ hget /sics/tc1/sensor/value ] " "] 2 ]
		broadcast "Current temperature is $curval"
		while {[ expr abs($curval - $cel_temperature) ] > 5 } {
			wait 60
			set curval [lindex [ split [ hget /sics/tc1/sensor/value ] " "] 2 ]
		}
		broadcast "Finished driving to $cel_temperature"
		wait 600
		runscan stth 2.75 5.2 50 time 190
	}
}

runtemps_up
