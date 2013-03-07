#
drive sc 0
drive msd 2500
sampledescription mtth140-noPC-noSC-Ge335-Magnet
title Proposal1560
user Precious Shamba
email ps807@uowmail.edu.au
#
# We want to run at 3 fields and 4 temperatures for one hour each
#
samplename La0.8Ce0.2(FeSi)13B1_0T_250K
drive tc2_driveable 250
# wait for equilibration with base
wait 1200       
runscan stth 4.0 5.2 25 time 190
# do 1T run
magnet send s 1.0
wait 300
samplename La0.8Ce0.2(FeSi)13B1_1T_250K
runscan stth 4.0 5.2 25 time 190
# do 6T run
magnet send s 6.0
wait 600
samplename La0.8Ce0.2(FeSi)13B1_6T_250K
runscan stth 4.0 5.2 25 time 190
#
#  Next temperature
#===========================
magnet send s 0.0
samplename La0.8Ce0.2(FeSi)13B1_0T_200K
drive tc2_driveable 200
# wait for equilibration with base
wait 1200       
runscan stth 4.0 5.2 25 time 190
# do 1T run
magnet send s 1.0
wait 300
samplename La0.8Ce0.2(FeSi)13B1_1T_200K
runscan stth 4.0 5.2 25 time 190
# do 6T run
magnet send s 6.0
wait 600
samplename La0.8Ce0.2(FeSi)13B1_6T_200K
runscan stth 4.0 5.2 25 time 190
#
#  Next temperature
#===========================
magnet send s 0.0
samplename La0.8Ce0.2(FeSi)13B1_0T_150K
drive tc2_driveable 150
# wait for equilibration with base
wait 1200       
runscan stth 4.0 5.2 25 time 190
# do 1T run
magnet send s 1.0
wait 300
samplename La0.8Ce0.2(FeSi)13B1_1T_150K
runscan stth 4.0 5.2 25 time 190
# do 6T run
magnet send s 6.0
wait 600
samplename La0.8Ce0.2(FeSi)13B1_6T_150K
runscan stth 4.0 5.2 25 time 190
#
#  Next temperature
#===========================

#  Next temperature - warm up
#===========================
