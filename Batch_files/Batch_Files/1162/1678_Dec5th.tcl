user "vep"
email "vep@ansto.gov.au"
phone "x9401"
title Mail-In Proposal 1678
sampledescription mtth140-noPC-noSC-Ge335
user Neeraj / Vanessa	

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 10
samplename Li6PS5I
hset sample/robby/setpoint 1
runscan stth 1.5 5.2 75 time 358
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 30
samplename LiMn2o4 MVR
hset sample/robby/setpoint 1
runscan stth 1.5 5.2 75 time 262
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 50
samplename LiFePO4 ex1
hset sample/robby/setpoint 1
runscan stth 1.5 5.2 75 time 142
hset sample/robby/setpoint 0
wait 60
