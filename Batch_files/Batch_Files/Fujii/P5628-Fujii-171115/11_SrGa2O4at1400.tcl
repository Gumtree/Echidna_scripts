#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
hsetprop /sample/tc1/setpoint tolerance 10
#
tc1 ramprate 1000
#----
user Kotaro Fujii
title Proposal 5628
# #--- List of temperatures
# proc runtemps_list {} {
# #tc1 ramprate 5000
# #drive tc1 700
# tc1 ramprate 1000
# set templist [list 200 400 600 800 900 1000]
# foreach cel_temperature $templist {
# samplename [ concat SrGe2O4-$cel_temperature ]
# # adjust West 400 max power to improve stability,
# # but no more than 45 percent
# set maxpower [expr $cel_temperature/19]
# if {$maxpower > 45} then {set maxpower 45}
# tc1 powermax $maxpower
# #hset /sample/tc1/setpoint $cel_temperature
# drive tc1_setpoint $cel_temperature
# wait 5
# drive tc1_setpoint $cel_temperature
# wait 1200
# runscan stth 1.5 5.125 30 time 380
# }
# }


# Do a room temperature run before starting
# samplename SrGe2O4-test (in Vac Furnace)
# runscan stth 1.5 5.125 30 time 190
# runtemps_list

# Manual HT-measurement
# tc1 ramprate 1000
# tc1 powermax 45
# drive tc1_setpoint 1200

# Temperature 1460C
# tc1 powermax 60
# drive tc1_setpoint 1350
# wait 5
# drive tc1_setpoint 1400
# wait 5
# tc1 ramprate 6
# drive tc1_setpoint 1460
# wait 1200

# measurement at 1400C
samplename  SrGe2O4-1400-2nd
runscan stth 1.5 5.125 30 time 1035

# Cooling
tc1 ramprate 10000
drive tc1_setpoint 0
