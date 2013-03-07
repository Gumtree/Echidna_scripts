# a simple RT run on sample
samplename ZrOCl2.6H2O RT measurement new detector module 3
runscan stth 2.75 5.2 50 time 622
# go to 55C
drive tc1_driveable 328
samplename ZrOCl2.6H2O at 55C new detector module 3
wait 600
runscan stth 2.75 5.2 50 time 622