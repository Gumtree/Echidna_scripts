user "njs"
email "njs@ansto.gov.au"
phone "x7253"
title Mail-In Proposal 1678
sampledescription mtth140-noPC-noSC-Ge335
user Neeraj / Manickam	



hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 20
samplename LiNiPO4 Quenched
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

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 40
samplename LiNiPO4 Charged Annealed
hset sample/robby/setpoint 1
wait 60
runscan stth 2.75 5.2 50 time 118
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 50
samplename LiNiPO4 Charged Quenched
hset sample/robby/setpoint 1
wait 60
runscan stth 2.75 5.2 50 time 118
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 39
samplename LiCoNiPO4 Charged
hset sample/robby/setpoint 1
wait 60
runscan stth 2.75 5.2 50 time 118
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 38
samplename Mn-Short
hset sample/robby/setpoint 1
wait 60
runscan stth 2.75 5.2 50 time 118
hset sample/robby/setpoint 0
wait 60

#--------------

hset sample/robby/control/pallet_nam b
hset sample/robby/control/target_loc Vacuum

#--------------
hset sample/robby/control/pallet_idx 37
samplename Mn-Long
hset sample/robby/setpoint 1
wait 60
runscan stth 2.75 5.2 50 time 118
hset sample/robby/setpoint 0
wait 60

#--------------
email "max@ansto.gov.au"
phone "x9522"
title Mail-In
sampledescription mtth140-noPC-noSC-VacCh-Ge335
user "Max Avdeev"

hset sample/robby/control/pallet_idx 22
samplename 1280048 1.62A
hset sample/robby/setpoint 1
wait 60
runscan stth 2.75 5.2 50 time 118
#hset sample/robby/setpoint 0
#wait 60
