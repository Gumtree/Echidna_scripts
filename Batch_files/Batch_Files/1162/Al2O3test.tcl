user "vep"
email "vep@ansto.gov.au"
phone "x9401"
title Mail-In Proposal 1678
sampledescription mtth140-noPC-noSC-Ge335
user Neeraj / Vanessa	



hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 1
samplename Al2O3 std
hset sample/robby/setpoint 1
runscan stth 4 5.2 25 time 80
hset sample/robby/setpoint 0
wait 60
