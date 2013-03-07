#Vacuum furnace run
sampledescription mtth140-noPC-noSC-Ge335
drive msd 2500
drive sc 0
user Henan Li
title Proposal 1214
# set up Vacuum Furnace
tc1 ramprate 300
tc1 PowerLimit 5
drive tc1 100
samplename H6_100C waiting
runscan stth 4.0 5.2 25 time 118
samplename H6_100C at 100C
runscan stth 4.0 5.2 25 time 838
# next temperature
tc1 PowerLimit 12
drive tc1 200
# wait one hour
samplename H6_200C waiting
runscan stth 5.0 5.2 25 time 118
samplename H6_200C at 200C
runscan stth 4.0 5.2 25 time 838
# next temperature
tc1 PowerLimit 50
drive tc1 1000
samplename H6_1000C at 1000C
runscan stth 4.0 5.2 25 time 838
#
drive tc1 10
#

