# Last two runs
samplename [ concat LuInFeO3, 300 K ]
# set cold head temperature
hset /sample/tc1/sensor/setpoint1 300
drive tc2_driveable 300
wait 300
runscan stth 2.75 5.2 50 time 347
# Final run at 320K
samplename [ concat LuInFeO3, 320 K ]
# set cold head temperature
hset /sample/tc1/sensor/setpoint1 320
drive tc2_driveable 320
wait 300
runscan stth 2.75 5.2 50 time 635
