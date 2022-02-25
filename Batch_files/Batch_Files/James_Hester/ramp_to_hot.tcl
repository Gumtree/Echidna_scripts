# Heat up CF7 from cold, then ramp to target temperature before measuring
# Quick measurement while heating
samplename CHS:WPA_90:10 cryo_heating
runscan stth 2.75 5.2 50 time 60
#
drive tc2_driveable 300
#
# set ramp rate
#
hset /sample/tc1/control/ramp_Loop_1 1,+6.000
hset /sample/tc1/control/ramp_Loop_2 1,+6.000
#
# heat to target temperature
hset /sample/tc1/sensor/setpoint1 443
hset /sample/tc1/sensor/setpoint2 443
#
drive tc1_driveable 443
drive tc1_driveable2 443
#
# Two measurements of 4hrs each
#
samplename CHS:WPA_90:10 170K
runscan stth 2.75 5.2 50 time 275
runscan stth 2.75 5.2 50 time 275
#
#
# No more ramping
#
hset /sample/tc1/control/ramp_Loop_1 0,+5.000
hset /sample/tc1/control/ramp_Loop_2 0,+5.000
#
hset /sample/tc1/sensor/setpoint1 4
hset /sample/tc1/sensor/setpoint2 4
#
hset /sample/tc2/sensor/setpoint1 4
#