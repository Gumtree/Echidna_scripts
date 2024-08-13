#
sampledescription mtth140-noPC-noSC-VF1-Ge335
hsetprop /sample/tc1/setpoint tolerance 10
#
tc1 ramprate 1000
#----
user Xiao-Qiang Liu
title MI13498
#--- List of temperatures
proc runtemps_list {} {
#tc1 ramprate 5000
#drive tc1 700
tc1 ramprate 1000
set templist [list 200 300 400 500 600 700 900 ]
foreach cel_temperature $templist {
samplename [ concat Li2Nd2Ti3O10-$cel_temperature ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 powermax $maxpower
#hset /sample/tc1/setpoint $cel_temperature
drive tc1_setpoint $cel_temperature
wait 5
drive tc1_setpoint $cel_temperature
wait 600
runscan stth 2.75 5.2 50 time 131
}
}


# Do a room temperature run before starting
#samplename CTO-25C (in Vac Furnace)
#runscan stth 2.75 5.2 50 time 203
runtemps_list
tc1 ramprate 10000
drive tc1_setpoint 0
