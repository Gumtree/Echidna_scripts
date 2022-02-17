# Cool down after change and then collect at temperatures
samplename beta-Ba2ScAlO5-cooldown
runscan stth 2.75 5.125 20 time 60
#hset /sample/tc1/sensor/setpoint1 4
drive tc2_driveable 5
hset /sample/tc2/sensor/setpoint1 4
drive tc1_driveable 5
hset /sample/tc1/sensor/setpoint1 4

#
samplename beta-Ba2ScAlO5_base
runscan stth 1.5 5.125 30 time 947
#
# Warm up
#
hset /sample/tc1/sensor/setpoint1 293
drive tc2_driveable 293
#
samplename beta-Ba2ScAlO5_RT
runscan stth 1.5 5.125 30 time 947
#