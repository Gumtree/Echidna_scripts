title Proposal 1404
sampledescription mtth100-noPC-noSC-Ge331
user Paul Saines
drive sc 0
drive msd 2500
#
# At base
#
samplename Coadipate at base,1.99A
runscan stth 2.75 5.2 50 time 262
#
# Warm up to 10K
#
drive tc1_driveable 10
wait 300
samplename Coadipate at 10 K,1.99A
runscan stth 2.75 5.2 50 time 262
#
# Warm up to 15K
#
drive tc1_driveable 15
wait 300
samplename Coadipate at 15K
runscan stth 4 5.2 50 time 262
#
# Warm up to 20K
#
drive tc1_driveable 20
wait 300
samplename Coadipate at 20 K,1.99A
runscan stth 2.75 5.2 50 time 262