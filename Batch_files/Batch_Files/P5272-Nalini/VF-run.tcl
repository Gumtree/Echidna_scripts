#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge331
#hsetprop /sample/tc1/setpoint tolerance 2
#
tc1 ramprate 1000
#----
#--- List of temperatures
proc runtemps_list {} {
tc1 ramprate 1000
set templist [list 700 900 1000 ]
foreach cel_temperature $templist {
drive tc1_setpoint $cel_temperature
wait 900
samplename [ concat LiDyMono at $cel_temperature C ]
runscan stth 2.75 5.2 50 time 131
}
}

# This is actually executed
samplename LiDyMono at RT
runscan stth 2.75 5.2 50 time 347
#
runtemps_list
#
samplename LiDyMono at 1100C
drive tc1_setpoint 1100
wait 900
runscan stth 2.75 5.2 50 time 347
#
tc1 ramprate 10000
drive tc1_setpoint 20
