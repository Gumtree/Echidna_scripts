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
tc1 ramprate 5000
drive tc1 700
tc1 ramprate 1000
set templist [list 800 ]
foreach cel_temperature $templist {
samplename [ concat PrBa0.2Sr0.8Co2O6 at $cel_temperature C ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 PowerLimit $maxpower
drive tc1 $cel_temperature
wait 600
runscan stth 4.0 5.146 12 time 552
}
}

proc runtemps_list_long {} {
set templist [list 800 ]
foreach cel_temperature $templist {
samplename [ concat PrBa0.2Sr0.8Co2O6 at $cel_temperature C ]
# adjust West 400 max power to improve stability,
# but no more than 45 percent
set maxpower [expr $cel_temperature/19]
if {$maxpower > 45} then {set maxpower 45}
tc1 PowerLimit $maxpower
drive tc1 $cel_temperature
wait 600
runscan stth 4.0 5.146 12 time 552
}
}

# Do a room temperature run before starting
# samplename PrBa0.2Sr0.8Co2O6 at RT (in Vac Furnace)
# runscan stth 4.0 5.146 12 time 276
runtemps_list
# runtemps_list_long
tc1 ramprate 10000
drive tc1 0
