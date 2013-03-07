drive sc 0
user Hugh Simons
title Proposal 1425
sampledescription mtth140-noPC-noSC-Ge331
sampletitle 94BNT-BT poled 8kV run2

drive som -90
samplename 94BNT-BT poled 8kV run2, 2.44A, omega -90
runscan stth 4.0 5.2 25 time 220	

drive som 0
samplename 94BNT-BT poled 8kV run2, 2.44A, omega 0
runscan stth 4.0 5.2 25 time 220

for {set i -80} {$i <= -10} {incr i 10} {
drive som [expr $i]
samplename [concat 94BNT-BT poled 8kV run2, 2.44A, omega $i]
runscan stth 4.0 5.2 25 time 220
#clientput $i
#set s [SplitReply [samplename]]
#clientput $s
#clientput [SplitReply [samplename]]
}

for {set i 10} {$i <= 90} {incr i 10} {
drive som [expr $i]
samplename [concat 94BNT-BT poled 8kV run2, 2.44A, omega $i]
runscan stth 4.0 5.2 25 time 220
#clientput $i
#set s [SplitReply [samplename]]
#clientput $s
#clientput [SplitReply [samplename]]
}
