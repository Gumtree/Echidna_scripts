#
sampledescription mtth140-noPC-noSC-VacFurnace-Ge335
hsetprop /sample/tc1/setpoint tolerance 2
#
tc1 ramprate 1000
#----
user Kotaro Fujii
title Proposal 4008

#samplename La2Mo2O9 at 1200 C test
#runscan stth 4 5.125 10 time 150
samplename La2Mo2O9 at 1200 C 1st
runscan stth 2.75 5.125 20 time 1000
samplename La2Mo2O9 at 1200 C 2nd
runscan stth 2.75 5.125 20 time 1000
tc1 ramprate 10000
drive tc1_setpoint 0