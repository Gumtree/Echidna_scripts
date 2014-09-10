# Collect a series of temperatures
# in the orange cryostat



samplename SrCu(VO4)OD at 20K
runscan stth 2.75 5.2 50 time 347
# now collect data
samplename SrCu(VO4)OD at 20K
runscan stth 2.75 5.2 50 time 347
# now base temperature
drive tc1_driveable 1.5
wait 300
# now collect data
samplename SrCu(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 347
# now collect data
samplename SrCu(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 347
#set templist [list 10 1.8]
#runtemps_up templist
drive tc1_driveable 10
