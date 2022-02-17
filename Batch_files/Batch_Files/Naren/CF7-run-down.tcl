drive tc1_driveable 293
drive tc2_driveable 293
wait 300

samplename MnNiCoTi_900_RT
runscan stth 2.75 5.2 50 time 203

# Set to 220 by going to 200 then heating up
hset /sample/tc1/sensor/setpoint1 220
hset /sample/tc1/sensor/setpoint2 220

# Funky way of getting to 220
drive tc2_driveable 200
drive tc1_driveable 220
drive tc2_driveable 220

wait 300

samplename MnNiCoTi_900_220K
runscan stth 2.75 5.2 50 time 203

# and now go to base
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4
drive tc2_driveable 4
drive tc1_driveable 4

wait 300
samplename MnNiCoTi_900_base
runscan stth 2.75 5.2 50 time 203

