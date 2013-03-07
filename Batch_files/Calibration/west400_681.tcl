gumput 1
drive msd 2500
gumput 2
drive sc 0
gumput 3
emon unregister tc1
gumput 4
broadcast emon behaves!
gumput 5
sampledescription mtth120-noPC-noSC-VacFurnace-331
gumput 6
sampletitle 
gumput 7
tc1 tolerance 500
gumput 8
#------------------
gumput 9
user Patryck Allen
gumput 10
title Proposal 681
gumput 11
samplename Ba2TiGe2O8 RT
gumput 12
runscan stth 4 5.2 25 time 406
gumput 13
#=======Next temperature....
gumput 14
drive tc1 800
gumput 15
wait 1800
gumput 16
samplename Ba2TiGe2O8 800C
gumput 17
runscan stth 4 5.2 25 time 406
gumput 18
#=================== Next temperature ...
gumput 19
drive tc1 900
gumput 20
wait 1800
gumput 21
samplename Ba2TiGe2O8 900C
gumput 22
runscan stth 4 5.2 25 time 406
gumput 23
#=================== Next temperature ...
gumput 24
drive tc1 1000
gumput 25
wait 1800
gumput 26
samplename Ba2TiGe2O8 1000C
gumput 27
runscan stth 4 5.2 25 time 406
gumput 28
#=================== Next temperature ...
gumput 29
drive tc1 20
gumput 30
#####End of experiment#####
