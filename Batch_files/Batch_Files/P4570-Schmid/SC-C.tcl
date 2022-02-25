#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
#hsetprop /sample/tc1/setpoint tolerance 2
#
tc1 ramprate 1000
#----
#--- List of temperatures
proc runtemps_list {} {
tc1 ramprate 1000
set templist [list 400 700 950 700 400 ]
foreach cel_temperature $templist {
set maxpower [expr $cel_temperature/19]
if {$maxpower > 20} then {set maxpower 20}
tc1 powermax $maxpower
drive tc1_setpoint $cel_temperature
wait 600
samplename [ concat SC-V at $cel_temperature C in vacuum]
runscan stth 2.75 5.2 50 time 419
}
}

# This is actually executed
samplename SC-V_RT
runscan stth 2.75 5.2 50 time 131
runtemps_list
tc1 ramprate 10000
drive tc1_setpoint 20
