user "njs"
email "njs@ansto.gov.au"
phone "x7253"
title Mail-In Proposal 1678
sampledescription mtth140-noPC-noSC-Ge335
user Neeraj / Manickam	

runscan stth 4 5.2 25 time 70
hset sample/robby/setpoint 0
wait 60
#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 10
samplename LiCoPo4 Annealed
hset sample/robby/setpoint 1
# drive robby_driveable 1
wait 60
runscan stth 1.5 5.2 75 time 166
hset sample/robby/setpoint 0
# drive robby_driveable 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 20
samplename LiCoPO4 Quenched
hset sample/robby/setpoint 1
wait 60
runscan stth 1.5 5.2 75 time 166
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 30
samplename LiCoNiPO4
hset sample/robby/setpoint 1
wait 60
runscan stth 1.5 5.2 75 time 166
hset sample/robby/setpoint 0
wait 60
