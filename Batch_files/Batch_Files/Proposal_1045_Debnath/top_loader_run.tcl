title Proposal 1045
sampledescription mtth140-noPC-SC10-Ge335
user Jyotish Debnath
#
# Sequence of temperatures using top loader and Lakeshore 336
#
samplename La0.7Ca0.3Mn03 at base
runscan stth 4.0 5.2 25 time 694
#
#  Next temperature
#
samplename La0.7Ca0.3Mn03 at 255K
drive tc1_driveable 255 tc1_driveable2 255
wait 600
runscan stth 4.0 5.2 25 time 694
#
#  Top temperature
#
samplename La0.7Ca0.3Mn03 at 275K
drive tc1_driveable 275 tc1_driveable2 275
wait 600
runscan stth 4.0 5.2 25 time 694