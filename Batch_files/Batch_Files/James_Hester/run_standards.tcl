# Running standards with scr in and small step size
samp_to_vac B2
samplename LaB6 with secondary collimator
runscan stth 2.75 5.225 100 time 60
#
samp_from_vac
samplename NAC with secondary collimator
samp_to_vac B3
runscan stth 2.75 5.225 100 time 60
#
# change to 2.43 A
drive mom 106.55
drive mchi -0.257
drive mf1 0.30
# Do it again
samplename NAC with secondary collimator
runscan stth 2.75 5.225 100 time 60
#
samp_from_vac
samplename LaB6 with secondary collimator
samp_to_vac B2
runscan stth 2.75 5.225 100 time 60
