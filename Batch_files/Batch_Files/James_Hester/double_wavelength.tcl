# to run a sample at two wavelengths
# 1.622
drive mchi -0.25
drive mom 70.14
drive mf1 0.26
samp_to_vac B3
sampledescription mtth140-noPC-noSC-VacCh-Ge335
samplename NAC at 1.62
runscan stth 2.75 5.2 50 time 60
#
drive mom 106.55
drive mchi -0.70
drive mf1 0.29
sampledescription mtth140-noPC-noSC-VacCh-Ge331
samplename NAC at 2.43
runscan stth 2.75 5.2 50 time 60
#
samp_from_vac 
samp_to_vac B47
samplename Ta2O5/SiO2 x=0.1
runscan stth 2.75 5.2 50 time 347
samp_from_vac

samp_to_vac B48
samplename Ta2O5/SiO2 x=0.2
runscan stth 2.75 5.2 50 time 347
samp_from_vac