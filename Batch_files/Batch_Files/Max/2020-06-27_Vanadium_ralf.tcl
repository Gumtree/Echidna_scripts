sampletitle
#---------------
config rights manager ansto
#--------------
email max@ansto.gov.au
phone +61 02 97179522

hset sample/ralf/control/pallet_nam a
hset sample/ralf/control/target_loc vacuum

drive mom 68.7 mchi -1.32 mf1 0.27
drive sx 0 sy 0
drive som 0
drive sphi 0 schi 90


#samplename dummy run
#runscan stth 2.75 2.80 1 MONITOR_3 600000 force true
#wait 3600

#--------------
#user Max Avdeev
#title Calibration
#sampledescription mtth140-noPC-noSC-VC-Ge335
#samplename Vanadium noPC-noSC-6mmrod, 1.6A
#hset sample/ralf/control/pallet_idx 5
#drive ralf_driveable 1
#hset sample/ralf/control/rotate 10
#runscan stth 2.75 5.2 50 time 1139
#hset sample/ralf/control/rotate 0
#wait 90
#drive ralf_driveable 0
#--------------
user Max Avdeev
title Calibration
sampledescription mtth140-noPC-noSC-VC-Ge335
samplename Background noPC-noSC-lid 1.6A
hset sample/ralf/control/pallet_idx 6
drive ralf_driveable 1
runscan stth 2.75 5.2 50 time 570
drive ralf_driveable 0
#--------------
