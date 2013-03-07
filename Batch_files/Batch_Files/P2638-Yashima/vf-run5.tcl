# Following lines needed because of temperature controller craziness
emon unregister tc1
broadcast emon behaves!
#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
tc1 tolerance 2
tc1 ramprate 1000
#----
#--- List of temperatures
proc runtemps_list {} {
#tc1 ramprate 5000
#drive tc1 700
tc1 ramprate 1000
set templist [list 400 600 800 1000 ]
foreach cel_temperature $templist {
samplename [ concat CaErAlO4 at $cel_temperature C ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 PowerLimit $maxpower
drive tc1 $cel_temperature
wait 600
runscan stth 2.75 5.146 24 time 230
}
}

proc runtemps_list_long {} {
set templist [list 1200 ]
foreach cel_temperature $templist {
samplename [ concat CaErAlO4 at $cel_temperature C ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 PowerLimit $maxpower
drive tc1 $cel_temperature
wait 600
runscan stth 2.75 5.146 24 time 720
}
}

# Do a room temperature run before starting
# samplename CaErAlO4 test (in Vac Furnace)
# runscan stth 4.0 5.146 12 time 60
runtemps_list
runtemps_list_long
tc1 ramprate 10000
drive tc1 0
