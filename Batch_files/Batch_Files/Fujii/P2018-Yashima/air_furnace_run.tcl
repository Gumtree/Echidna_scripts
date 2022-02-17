# Collect a series of temperatures
# in the air furnace using invisible sics
# internal tree

proc runtemps_up {} {
	set templist [list 400 600 800]
	foreach cel_temperature $templist {
		samplename [ concat CaYAlO4 4cmAluminaHolder in AirFurnace, $cel_temperature C ]
		hset /sics/tc1/setpoint $cel_temperature
		wait 1
		set curval [lindex [ split [ hget /sics/tc1/sensor/value ] " "] 2 ]
		broadcast "Current temperature is $curval"
		while {[ expr abs($curval - $cel_temperature) ] > 5 } {
			wait 60
			set curval [lindex [ split [ hget /sics/tc1/sensor/value ] " "] 2 ]
		}
		broadcast "Finished driving to $cel_temperature"
		wait 300
		runscan stth 4.0 5.2 13 time 177
	}
}

proc run_onethousand {} {
	samplename [ concat CaYAlO4 4cmAluminaHolder in AirFurnace, 1000 C ]
	hset /sics/tc1/setpoint 1000
	wait 1
	set curval [lindex [ split [ hget /sics/tc1/sensor/value ] " "] 2 ]
	broadcast "Current temperature is $curval"
	while {[ expr abs($curval - 1000) ] > 5 } {
		wait 60
		set curval [lindex [ split [ hget /sics/tc1/sensor/value ] " "] 2 ]
	}
	broadcast "Finished driving to 1000"
	wait 300
	runscan stth 4.0 5.2 25 time 530
}

runtemps_up
run_onethousand
