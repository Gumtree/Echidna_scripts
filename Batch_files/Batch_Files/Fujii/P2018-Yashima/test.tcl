# Collect a series of temperatures
# in the air furnace using invisible sics
# internal tree

proc runtemps_up {} {
	set templist [list 4.0 4.1]
	foreach cel_temperature $templist {
		samplename [ concat CaYAlO4 4cmAluminaHolder in AirFurnace, $cel_temperature C ]
		# hset /sics/tc1/sensor/setpoint $cel_temperature
		set curval [lindex [ split [ hget /sample/azimuthal_angle ] " "] 2 ]
		broadcast $curval
		while {[expr abs($curval - $cel_temperature) ] > 0.01 } {
			# puts [ expr {abs($curval - $cel_temperature)}]
			wait 6
			set curval [ lindex [split [ hget /sample/azimuthal_angle ] " "] 2 ]
			broadcast [expr abs($curval - $cel_temperature)]
		}
		wait 3
		broadcast "runscan stth 4.0 5.2 13 time 177"
	}
}

runtemps_up
#samplename [ concat CaYAlO4 4cm Alumina holder in Air furnace, 1000 C ]
#hset /sics/tc1/sensor/setpoint 1000
#wait 300
#runscan stth 4.0 5.2 25 time 530