#
hset /sample/tc1/sensor/setpoint1 3
hset /sample/tc1/sensor/setpoint2 3
hset /sample/tc2/sensor/setpoint1 3

# make sure the heaters are actually on
hset /sample/tc1/heater/heaterrange_1 3
hset /sample/tc1/heater/heaterrange_2 3
hset /sample/tc2/heater/heaterrange_1 5
drive tc1_driveable 4
#