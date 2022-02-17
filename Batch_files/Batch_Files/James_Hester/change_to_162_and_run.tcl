# to run a sample at two wavelengths
# 1.622
drive mchi -1.32
drive mom 68.7
drive mf1 0.27
samp_to_vac A45
sampledescription mtth140-noPC-noSC-VacCh-Ge335
samplename BWVO_test
runscan stth 2.75 5.2 50 time 131
samp_from_vac