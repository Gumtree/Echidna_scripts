# Running in orange cryostat
# Finish 100K run
samplename LuInFeO3_100K_second
runscan stth 2.75 5.2 50 time 311
# Now go to 150K
drive tc1_driveable 150
samplename LuInFeO3_150K_full
wait 900
runscan stth 2.75 5.2 50 time 635