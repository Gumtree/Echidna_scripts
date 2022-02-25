


hset /sample/tc1/temp0/setpoint 100


drive tc1_temp0_setpoint 100
wait 900

samplename CoMg3Nb2O9 at 100K, 0T
runscan stth 2.75 5.2 50 time 206


hset /sample/tc1/temp0/setpoint 200

drive tc1_temp0_setpoint 200
wait 900

samplename CoMg3Nb2O9 at 200K, 0T
runscan stth 2.75 5.2 50 time 206

hset /sample/tc1/temp0/setpoint 300

drive tc1_temp0_setpoint 300
wait 900

samplename CoMg3Nb2O9 at 300K, 0T
runscan stth 2.75 5.2 50 time 206

