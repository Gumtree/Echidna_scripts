#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
hsetprop /sample/tc1/setpoint tolerance 10
#
tc1 ramprate 1000
#----
user Kotaro Fujii
title Proposal 7589
#--- List of temperatures
proc runtemps_list {} {
#tc1 ramprate 5000
#drive tc1 700
tc1 ramprate 1000
set templist [list 200 400 600 800 1000 1100 1200 1300 1400 1450 1500 1550 1600]
foreach cel_temperature $templist {
samplename [ concat La2Ti2O7-$cel_temperature ]
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
runscan stth 1.5 5.125 30 time 110
# if {$cel_temperature < 700} then {runscan stth 1.5 5.125 30 time 160}
# if {$cel_temperature > 700} then {runscan stth 1.5 5.125 30 time 400}
}
}


# Do a room temperature run before starting
samplename La2Ti2O7-test (in Vac Furnace)
runscan stth 1.5 5.125 30 time 20
runtemps_list
tc1 ramprate 10000
drive tc1_setpoint 0
