drive sc 0
user Hugh Simons
title Proposal 1425
sampledescription mtth140-noPC-noSC-Ge331
sampletitle 94BNT-BT poled 8kV
for {set i -90} {$i <= 90} {incr i 10} {

drive som [expr $i]
samplename [concat 94BNT-BT poled 8kV, 2.44A, omega $i]
runscan stth 4.0 5.2 25 time 262	

#clientput $i
#set s [SplitReply [samplename]]
#clientput $s
#clientput [SplitReply [samplename]]
	
}
