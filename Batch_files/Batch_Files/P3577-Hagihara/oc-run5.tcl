# Collect a series of temperatures
# in the orange cryostat


samplename CaNi(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 361

samplename CaNi(VO4)OD at 1.5K
runscan stth 2.75 5.2 50 time 361

drive tc1_driveable 10
wait 300

samplename CaNi(VO4)OD at 10K
runscan stth 2.75 5.2 50 time 361

samplename CaNi(VO4)OD at 10K
runscan stth 2.75 5.2 50 time 361


