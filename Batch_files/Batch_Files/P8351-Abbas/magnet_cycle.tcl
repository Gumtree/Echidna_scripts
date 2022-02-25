# Cycle the magnet at 50K
proc gotofield {last_field next_field ramprate} {
broadcast going from $last_field to $next_field
oxfordsetrate $ramprate
oxfordseths on
# need to wait for the power supply to ramp up at 10s/T plus 30sec wait
set initial_wait_time [expr {(abs($last_field)*10 + 60)}]
set wait_time [expr {((abs($next_field - $last_field)/$ramprate)*60 + 60)}]
broadcast Power supply ramp up for $initial_wait_time
wait $initial_wait_time
oxfordsetfield $next_field
broadcast Waiting for $wait_time
wait $wait_time
oxfordseths off
wait 60
}

set last_field 0

gotofield 0 7 0.5

samplename NiO_nano 50K 7T first time
runscan stth 2.75 5.125 20 time 703

# Now go to the reverse

gotofield 7 -7 0.3

samplename NiO_nano 50K -7T first time
runscan stth 2.75 5.125 20 time 703

# And back again...

gotofield -7 7 0.3
samplename NiO_nano 50K 7T second time
runscan stth 2.75 5.125 20 time 703
