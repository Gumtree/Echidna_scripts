# Run at current temperature and then go cold
# samplename Cr2CoAl_400K
# runscan stth 2.75 5.2 50 time 347
#
# Now cool down
hset /sample/tc2/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint1 100
drive tc1_driveable2 100
drive tc2_driveable 100
# collect data
samplename Cr2.2Co0.8Al_100K
runscan stth 2.75 5.2 50 time 347
# now return to RT
#hset /sample/tc1/sensor/setpoint1 300
#hset /sample/tc1/sensor/setpoint2 300
#drive tc2_driveable 300
#