# Running the triton at low temperature
set templist [ list 1.0 0.75 0.5 0.25 ]

# wait for the beam to come up
# runscan stth 4.0 4.05 1 MONITOR_2 500000 force true
# 6 x 1hr runs
samplename TbODCO3 at 1.25K

for {set x 0} {$x<6} {incr x} {
	runscan stth 2.75 5.2 50 time 60
}

triton SetPI 10 100

foreach t $templist {
	triton SetTemp $t
	samplename [ concat TbOdCO3 $t K ]
	triton TempWait $t
	wait 300
	for {set x 0} {$x<6} {incr x} {
		runscan stth 2.75 5.2 50 time 60
	}
}