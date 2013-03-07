#
drive sc 0
drive msd 2500
sampledescription mtth140-noPC-noSC-Ge335-VacCh
title Proposal1560
user Precious Shamba
email ps807@uowmail.edu.au
#
hset /sample/robby/control/Pallet_Nam B
hset /sample/robby/control/Target_Loc VACUUM
#
samplename La0.8Ce0.2(FeSi)13B0.03
hset /sample/robby/control/Pallet_Idx 43
drive robby_driveable 1
runscan stth 4.0 5.2 25 time 118
drive robby_driveable 0
#
samplename La0.8Ce0.2(FeSi)13
hset /sample/robby/control/Pallet_Idx 42
drive robby_driveable 1
runscan stth 4.0 5.2 25 time 118
drive robby_driveable 0
#
samplename La0.8Ce0.2(FeSi)13B1.0
hset /sample/robby/control/Pallet_Idx 44
drive robby_driveable 1
runscan stth 4.0 5.2 25 time 118
drive robby_driveable 0
#
samplename LaFe11.7Si1.3
hset /sample/robby/control/Pallet_Idx 45
drive robby_driveable 1
runscan stth 4.0 5.2 25 time 118
drive robby_driveable 0