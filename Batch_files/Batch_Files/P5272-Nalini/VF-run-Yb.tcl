#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge331
#hsetprop /sample/tc1/setpoint tolerance 2
#
tc1 ramprate 1000
#----
#--- List of temperatures
proc runtemps_list {} {
tc1 ramprate 1000
set templist [list 700 900 1000 1100 ]
foreach cel_temperature $templist {
drive tc1_setpoint $cel_temperature
wait 900
samplename [ concat LiYbMono at $cel_temperature C ]
runscan stth 2.75 5.2 50 time 131
}
}

# This is actually executed
samplename LiYbMono at RT
runscan stth 2.75 5.2 50 time 347
#
runtemps_list
#
samplename LiYbMono at 1150C
drive tc1_setpoint 1150
wait 900
runscan stth 2.75 5.2 50 time 347
#
tc1 ramprate 10000
drive tc1_setpoint 20
