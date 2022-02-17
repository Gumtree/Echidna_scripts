# Created by J Hester based on previous work by Max and Andrew
# Collect data at multiple temperatures

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

# Remove remanent field, assumes starting at
# below 5.5T as uses maximum ramp rate
proc degauss {start_field} {
oxfordseths on
wait 120
set ramprate 0.45
set last_field $start_field
while {abs($last_field)>0.05} {
set next_field [expr {$last_field * -0.5}]
set wait_time [expr {((abs($next_field - $last_field)/$ramprate)*60 + 30)}]
broadcast Next field $next_field waiting $wait_time s
oxfordsetfield $next_field
wait $wait_time
set last_field $next_field
}
oxfordsetfield 0.0
wait 30
oxfordseths off
wait 60
}

# Note that this routine assumes a ramp rate of 0.45
# and will therefore get it wrong at high fields in
# fast mode.
proc reset_field {final_field} {
hset /sample/tc1/temp0/setpoint 170
degauss $final_field
set last_field 0.0 
drive tc1_temp0_setpoint 170
}

#---stuff happens after this line ---
reset_field 0

# set temperature to 75
hset /sample/tc1/pres8/setpoint 20
drive tc1_temp0_setpoint 75
hset /sample/tc1/pres8/setpoint 5
wait 900

set last_field 0.0
set fieldlist [list 0.5 1 2 3 5 7 ]

foreach one_field $fieldlist {
	gotofield $last_field $one_field 0.45
	set last_field $one_field
	samplename FeSbO4_75K, $one_field T
	runscan stth 2.75 5.2 50 time 275 
}

reset_field 7



### 
