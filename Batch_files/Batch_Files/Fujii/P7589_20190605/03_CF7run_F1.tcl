#
sampledescription mtth140-noPC-noSC-CF7-Ge335
#
user Kotaro Fujii
title Proposal 7589
hset /sample/tc1/heater/heaterrange_1 3
hset /sample/tc1/heater/heaterrange_2 3
#--- List of temperatures
proc runtemps_list {} {
set templist [list 293 333 363 393]
foreach kel_temperature $templist {
samplename [ concat La12Sr18Mn2O7F-$kel_temperature ]
hset /sample/tc1/sensor/setpoint1 $kel_temperature
	drive tc1_driveable2 $kel_temperature
wait 900
runscan stth 1.5 5.125 30 time 340
# if {$kel_temperature < 700} then {runscan stth 1.5 5.125 30 time 160}
# if {$kel_temperature > 700} then {runscan stth 1.5 5.125 30 time 400}
}
}


# Do a room temperature run before starting
runtemps_list
hset /sample/tc1/sensor/setpoint1 293
drive tc1_driveable2 293
