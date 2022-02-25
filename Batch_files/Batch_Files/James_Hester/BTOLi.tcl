# Measure at RT 4K 200K
samplename BTOLi0.05 at RT
runscan stth 2.75 5.2 50 time 347

samplename BTOLi0.05 at 100K
hset /sample/tc1/sensor/setpoint1 110
hset /sample/tc1/sensor/setpoint2 110
drive tc2_driveable 50
drive tc1_driveable 110
drive tc2_driveable 110
wait 300

runscan stth 2.75 5.2 50 time 347

samplename BTOLi0.05 at 250K
hset /sample/tc1/sensor/setpoint1 250
hset /sample/tc1/sensor/setpoint2 250
drive tc2_driveable 250
wait 300

runscan stth 2.75 5.2 50 time 347