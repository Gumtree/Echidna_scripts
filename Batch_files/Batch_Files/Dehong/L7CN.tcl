title P1228  
sampledescription mtth140-noPC-noSC-CF7-Ge335
user Shuhua Yao
sampletitle L7CN
#tc2 - 336 (sample space),tc1 - 340 (stick) 

#samplename L7CN cooling
#runscan stth 4 5.2 25 time 118

hset sample/tc1/control/tolerance1 1
hset sample/tc2/control/tolerance1 1

hset sample/tc1/heater/heaterrange_1 3
hset sample/tc2/heater/heaterrange 5

#base temperature
#drive tc2_driveable 3.5
#drive tc1_driveable 3.5
#samplename L7CN base T
#runscan stth 4.0 5.2 25 time 190
#runscan stth 4.0 5.2 25 time 190

#for {set i 10} {$i <= 90} {incr i 10} {
#drive tc2_driveable 5
#hset sample/tc1/heater/heaterRange_1 3
#hset /sample/tc1/sensor/setpoint1 [expr $i]
#hset /sample/tc2/sensor/setpoint1 [expr $i]
#drive tc2_driveable [expr $i]
#drive tc1_driveable [expr $i]
#wait 900
#samplename [concat L7CN, $i K ]
#runscan stth 4.0 5.2 25 time 190
#runscan stth 4.0 5.2 25 time 190
#}


for {set i 10} {$i <= 90} {incr i 10} {
drive tc2_driveable [expr $i] tc1_driveable [expr $i]
wait 300
samplename [concat L7CN, $i K ]
runscan stth 4.0 5.2 25 time 190
runscan stth 4.0 5.2 25 time 190
}
