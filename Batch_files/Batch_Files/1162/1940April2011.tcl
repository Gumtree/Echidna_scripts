#hset sample/robby/control/pallet_nam b
#hset sample/robby/control/target_loc Vacuum

#drive mom 69.98
#drive mchi -0.21
#drive mf1 0.259
sampledescription "mtth140-noPC-SC-VacCh-Ge335"

#--------------
#hset sample/robby/control/pallet_idx 1
#user Neeraj Sharma
#samplename Mail In 1940 Al2O3
#drive robby_driveable 1
#runscan stth 4 5.2 25 time 90
#drive robby_driveable 0
#--------------

#--------------
#hset sample/robby/control/pallet_idx 46
user Neeraj Sharma
samplename Mail In 1940 Li2Mg0.45Mn0.55SiO4
#drive robby_driveable 1
runscan stth 1.5 5.2 75 time 406
drive robby_driveable 0
#--------------

#--------------
hset sample/robby/control/pallet_idx 48
user Neeraj Sharma
samplename Mail In 1940 Li2Mg0.5Mn0.5SiO4
drive robby_driveable 1
runscan stth 1.5 5.2 75 time 406
drive robby_driveable 0
#--------------
