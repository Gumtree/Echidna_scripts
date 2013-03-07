user "vep"
email "vep@ansto.gov.au"
phone "x9401"
title "MOF-5 d 20K"
samplename "MOF-5 d 20K"
sampledescription "mtth120-noPC-noSC-SampCh"
tc1 tolerance 2
tc2 tolerance 2
tc1 controlsensor sensorA
tc2 controlsensor sensorA
tc1 range 5
tc2 range 4
drive tc1 20 tc2 20
wait 300
runscan stth 4 5.2 25 time 576
runscan stth 4 5.2 25 time 576
title "MOF-5 d 50K"
samplename "MOF-5 d 50K"
tc1 tolerance 2
tc2 tolerance 2
drive tc1 50 tc2 50
wait 600
runscan stth 4 5.2 25 time 432
runscan stth 4 5.2 25 time 432
title "MOF-5 d 100K"
samplename "MOF-5 d 100K"
tc1 tolerance 2
tc2 tolerance 2
drive tc1 100 tc2 100
wait 900
runscan stth 4 5.2 25 time 432
runscan stth 4 5.2 25 time 432
title "MOF-5 d 200K"
samplename "MOF-5 d 200K"
tc1 tolerance 3
tc2 tolerance 3
drive tc1 200 tc2 200
wait 900
runscan stth 4 5.2 25 time 432
runscan stth 4 5.2 25 time 432
title "MOF-5 d 300K"
samplename "MOF-5 d 300K"
tc1 tolerance 3
tc2 tolerance 3
drive tc1 300 tc2 300
wait 1800
runscan stth 4 5.2 25 time 576
runscan stth 4 5.2 25 time 576
title "MOF-5 d 400K"
samplename "MOF-5 d 400K"
tc1 tolerance 4
tc2 tolerance 4
drive tc1 400 tc2 400
wait 2100
runscan stth 4 5.2 25 time 432
runscan stth 4 5.2 25 time 432