hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

drive mom 69.96
drive mchi -0.23
drive mf1 0.259
sampledescription "mtth140-noPC-SC-VacCh-Ge335"

#--------------
hset sample/robby/control/pallet_idx 1
user Neeraj Sharma
samplename Mail In 1941 Al2O3
drive robby_driveable 1
runscan stth 4 5.2 25 time 90
drive robby_driveable 0
#--------------

#--------------
hset sample/robby/control/pallet_idx 50
user Neeraj Sharma
samplename Mail In 1941 PVDF
drive robby_driveable 1
runscan stth 1.5 5.2 75 time 70
drive robby_driveable 0
#--------------

#--------------
#hset sample/robby/control/pallet_idx XX
#user Neeraj Sharma
#samplename Mail In 1941 LSTN 018 5 days at 55C
#drive robby_driveable 1
#runscan stth 1.5 5.2 75 time 838
#drive robby_driveable 0
#--------------
