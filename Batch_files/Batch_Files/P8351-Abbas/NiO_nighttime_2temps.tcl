samplename Sample_12 base
runscan stth 2.75 5.125 20 time 707

samplename Sample_12 12K
hset /sample/tc1/sensor/setpoint1 12
drive tc2_driveable 12
runscan stth 2.75 5.125 20 time 707

hset /sample/tc1/sensor/setpoint1 44
drive tc2_driveable 44

samplename Sample_12 44K
runscan stth 2.75 5.125 20 time 707

hset /sample/tc1/sensor/setpoint1 112
drive tc2_driveable 112

samplename Sample_12 112K
runscan stth 2.75 5.125 20 time 707

hset /sample/tc1/sensor/setpoint1 300
drive tc2_driveable 300

samplename Sample_12 300K
runscan stth 2.75 5.125 20 time 707
