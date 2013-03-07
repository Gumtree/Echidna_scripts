user "vep"
email "vep@ansto.gov.au"
phone "x9401"
title "MOF-5 d 400K"
samplename "MOF-5 d 400K"
tc1 controlsensor sensorA
tc2 controlsensor sensorA
tc1 range 5
tc2 range 4
tc1 tolerance 4
tc2 tolerance 4
drive tc1 400 tc2 400
wait 2100
runscan stth 4 5.2 25 time 432
runscan stth 4 5.2 25 time 432

