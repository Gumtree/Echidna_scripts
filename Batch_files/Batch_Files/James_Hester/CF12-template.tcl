sampledescription mtth140-noPC-noSC-CF12-Ge335

samplename TbCr0.9Mn0.1O3 at base
runscan stth 2.75 5.2 50 time 311

set templist [list 70 200 300 ]
foreach temperature $templist {
hset sample/tc1/temp0/setpoint $temperature
wait 600
samplename [concat TbCr0.9Mn0.1O3 $temperature K ]
runscan stth 2.75 5.2 50 time 311
}

hset sample/tc1/temp0/setpoint 1.3
 
