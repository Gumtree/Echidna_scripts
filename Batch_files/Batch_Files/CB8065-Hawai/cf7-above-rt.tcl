# Collect a series of temperatures
# in the top loader

set smpname [SplitReply [samplename]]

proc runtemps_above_rt {templist sampname} {
	foreach kel_temperature $templist {
		samplename [ concat $sampname $kel_temperature K ]
		# do not set cold head temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		drive tc1_driveable $kel_temperature
		wait 120
		runscan stth 2.75 5.125 20 time 62
	}
}

hset /sample/tc1/heater/heaterRange_1 5
hset /sample/tc1/heater/heaterRange_2 5
hset /sample/tc2/sensor/setpoint1 300

# First measure at 400
samplename [ concat $smpname 400 ]
hset /sample/tc1/sensor/setpoint2 400
drive tc1_driveable 400
wait 300
runscan stth 2.75 5.125 20 time 527

# 2nd measure at 500
samplename [ concat $smpname 500 ]
hset /sample/tc1/sensor/setpoint2 500
drive tc1_driveable 500
wait 300
runscan stth 2.75 5.125 20 time 527

runtemps_above_rt [list 510 520 530 540 550 560 570 580 590 600 610 620 630 640 ]

# Finish at 650
samplename [ concat $smpname 650 ]
hset /sample/tc1/sensor/setpoint2 650
drive tc1_driveable 650
wait 300
runscan stth 2.75 5.125 20 time 527

hset /sample/tc2/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4