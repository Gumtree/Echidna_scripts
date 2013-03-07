# template for Eulerian cradle run
title Proposal 1530
sampledescription mtth140-noPC-noSC-Eulerian-Ge335
user Kabra Liss Yan
#
samplename FeSMA_random70_sample5
#
# rotate around chi
for {set mychi 0} {$mychi < 91} {incr mychi 45} {
	drive echi $mychi
	for {set myphi 0} {$myphi < 181} {incr myphi 45} {
	samplename [concat FeSMA_random70_sample5, at chi = $mychi and phi = $myphi]
	# move to next chi
	drive ephi $myphi
	# broadcast $myphi $mychi
	# collect data for one hour
	runscan stth 4.0 5.2 25 time 118
	}
}
