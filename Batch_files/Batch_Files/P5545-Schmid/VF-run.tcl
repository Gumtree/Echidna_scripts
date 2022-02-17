#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge331
#hsetprop /sample/tc1/setpoint tolerance 2
#
tc1 ramprate 1000
#----
#--- List of temperatures
proc runtemps_list {} {
tc1 ramprate 1000
set templist [list 200 400 600 800 1000 ]
foreach cel_temperature $templist {
set maxpower [expr $cel_temperature/19]
if {$maxpower > 20} then {set maxpower 20}
tc1 powermax $maxpower
drive tc1_setpoint $cel_temperature
wait 900
samplename [ concat Ta2O5-SiO2 0.1 at $cel_temperature C in quartz/Pt/air]
runscan stth 2.75 5.2 50 time 213
}
}

# This is actually executed
samplename Ta2O5-SiO2 0.1 at RT
runscan stth 2.75 5.2 50 time 60 

runtemps_list

tc1 ramprate 10000
drive tc1_setpoint 20
