# Cool down after change and then collect at temperatures
samplename Fe3GaTe2_400K
runscan stth 2.75 5.2 50 time 347

# Now cool down to base
hset /sample/tc1/sensor/setpoint1 2
hset /sample/tc2/sensor/setpoint1 4
hset /sample/tc2/sensor/setpoint2 4
#
drive tc2_driveable 5
#
drive tc2_driveable2 5
#
drive tc1_driveable 5
#
samplename Fe3GaTe2_base
runscan stth 2.75 5.2 50 time 347

# Surprise ! Not making hot after all