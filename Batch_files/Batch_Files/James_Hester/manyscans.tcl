# Initially do 4 x 30min runs at base
samplename TbODCO3 at base
for {set x 0} {$x<4} {incr x} {
	runscan stth 2.75 5.125 20 time 60
}
