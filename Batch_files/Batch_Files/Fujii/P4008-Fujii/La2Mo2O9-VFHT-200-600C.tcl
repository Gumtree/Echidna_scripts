#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
hsetprop /sample/tc1/setpoint tolerance 2
#
tc1 ramprate 1000
#----
user Kotaro Fujii
title Proposal 4008
#--- List of temperatures
proc runtemps_list {} {
#tc1 ramprate 5000
#drive tc1 700
tc1 ramprate 1000
set templist [list 200 400 600 ]
foreach cel_temperature $templist {
samplename [ concat La2Mo2O9 at $cel_temperature C ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 powermax $maxpower
#hset /sample/tc1/setpoint $cel_temperature
drive tc1_setpoint $cel_temperature
wait 1200
runscan stth 2.75 5.125 20 time 300
}
}

runtemps_list

