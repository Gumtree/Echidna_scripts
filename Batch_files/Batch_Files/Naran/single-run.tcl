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
wait 60
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

proc reset_field {final_field} {
hset /sample/tc1/Loop1/setpoint 50
degauss $final_field
set last_field 0.0

# cool to 4K
#hset /sample/tc1/Loop1/setpoint 10
#samplename Cooling Mn3V2O8 from 50 to 10
#radcollrun 1 15
#hset /sample/tc1/Loop1/setpoint 4
#samplename Cooling Mn3V2O8 from 10 to 4
#radcollrun 1 10
}


#--------------stuff happens here
gotofield 0 10.0 0.45

samplename La2CoIrO6 at 1.5K at 10T scan 1
runscan stth 2.75 5.2 50 time 347
#
samplename La2CoIrO6 at 1.5K at 10T scan 2
runscan stth 2.75 5.2 50 time 347

