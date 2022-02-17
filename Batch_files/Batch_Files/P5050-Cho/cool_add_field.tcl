# cooldown then apply magnetic field
proc runtemps_up_full {} {
set templist [list 20  27 30 35 40 ]
foreach one_temp $templist {
	samplename [ concat HS37 at $one_temp K in 3T field]
	hset /sample/tc1/sensor/setpoint1 $one_temp
	drive tc1_driveable2 $one_temp
	wait 600
	runscan stth 2.75 5.2 50 time 419
}
}

proc runtemps_up_part {} {
set templist [list 30 35 40 ]
foreach one_temp $templist {
	samplename [ concat HS37 at $one_temp K in 5T field]
	hset /sample/tc1/sensor/setpoint1 $one_temp
	drive tc1_driveable2 $one_temp
	wait 600
	runscan stth 2.75 5.2 50 time 419
}
}

#runtemps_up_part
# warm up
#hset /sample/tc1/sensor/setpoint1 60
#hset /sample/tc1/sensor/setpoint2 60
#drive magnet1_setpoint 0
#drive tc1_driveable2 60
#wait 600
#hset /sample/tc1/sensor/setpoint1 15
#drive tc1_driveable2 15
#wait 600
drive magnet1_setpoint 3
# now collect data
runtemps_up_full