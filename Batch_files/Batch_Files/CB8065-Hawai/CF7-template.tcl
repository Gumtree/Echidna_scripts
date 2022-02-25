# Collect a series of temperatures
# in the top loader

set smpname [SplitReply [samplename]]

proc runtemps_up {templist sampname} {
	foreach kel_temperature $templist {
		samplename [ concat $sampname $kel_temperature K ]
		# set cold head temperature
		hset /sample/tc1/sensor/setpoint1 $kel_temperature
		hset /sample/tc1/sensor/setpoint2 $kel_temperature
		hset /sample/tc1/heater/heaterRange_2 5
		drive tc2_driveable $kel_temperature
		hset /sample/tc1/heater/heaterRange_2 5
		wait 300
		runscan stth 2.75 5.125 20 time 527
	}
}

#get to base
hset /sample/tc2/sensor/setpoint1 4
drive tc1_driveable 5
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc2/sensor/setpoint1 4
drive tc1_driveable 4
wait 300
samplename [concat $smpname base]
runscan stth 2.75 5.125 20 time 2147
runtemps_up [list 100 200 ] $smpname

hset /sample/tc1/sensor/setpoint1 300
hset /sample/tc1/sensor/setpoint2 300
drive tc2_driveable 300
wait 300
samplename [concat $smpname 300 K]
runscan stth 2.75 5.125 20 time 1067
# reset samplename
samplename $smpname