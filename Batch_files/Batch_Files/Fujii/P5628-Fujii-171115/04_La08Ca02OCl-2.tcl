#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
hsetprop /sample/tc1/setpoint tolerance 10
#
tc1 ramprate 1000
#----
user Kotaro Fujii
title Proposal 5628
#--- List of temperatures
proc runtemps_list {} {
#tc1 ramprate 5000
#drive tc1 700
tc1 ramprate 1000
set templist [list 200 400 600]
foreach cel_temperature $templist {
samplename [ concat La08Ca02OCl-$cel_temperature ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 powermax $maxpower
#hset /sample/tc1/setpoint $cel_temperature
drive tc1_setpoint $cel_temperature
wait 5
drive tc1_setpoint $cel_temperature
wait 1200
runscan stth 1.5 5.125 30 time 390
}
}

proc runtemps_list_HT {} {
#tc1 ramprate 5000
#drive tc1 700
tc1 ramprate 1000
set templist [list 800 900 1000]
foreach cel_temperature $templist {
samplename [ concat La08Ca02OCl-1st-$cel_temperature ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 powermax $maxpower
#hset /sample/tc1/setpoint $cel_temperature
drive tc1_setpoint $cel_temperature
wait 5
drive tc1_setpoint $cel_temperature
wait 1200
runscan stth 1.5 5.125 30 time 130
samplename [ concat La08Ca02OCl-2nd-$cel_temperature ]
runscan stth 1.5 5.125 30 time 390
}
}

# Do a room temperature run before starting
samplename La08Ca02OCl-test (in Vac Furnace)
runscan stth 1.5 5.125 30 time 195
runtemps_list
runtemps_list_HT
tc1 ramprate 10000
drive tc1_setpoint 0
