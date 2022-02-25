# Collect at RT after change and then collect at temperatures
samplename Ba2LuAlO5_RT
runscan stth 1.5 5.125 30 time 947
hset /sample/tc1/sensor/setpoint1 4
drive tc2_driveable 5
hset /sample/tc2/sensor/setpoint1 4
drive tc1_driveable 5
hset /sample/tc1/sensor/setpoint1 4

#
samplename Ba2LuAlO5_base
runscan stth 1.5 5.125 30 time 947
