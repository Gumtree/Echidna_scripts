hset /sample/tc1/pres8/setpoint 30
wait 2000
hset /sample/tc1/pres8/setpoint 6
drive tc1_temp0_setpoint 1
wait 1500




samplename Mg4Nb2O9 at 1.6K, 0T
runscan stth 2.75 5.2 50 time 206




hset /sample/tc1/temp0/setpoint 50


drive tc1_temp0_setpoint 50
wait 900

samplename Mg4Nb2O9 at 50K, 0T
runscan stth 2.75 5.2 50 time 206


hset /sample/tc1/temp0/setpoint 200

drive tc1_temp0_setpoint 200
wait 1500

samplename Mg4Nb2O9 at 200K, 0T
runscan stth 2.75 5.2 50 time 206

hset /sample/tc1/temp0/setpoint 300

drive tc1_temp0_setpoint 300
wait 1500

samplename Mg4Nb2O9 at 300K, 0T
runscan stth 2.75 5.2 50 time 206

