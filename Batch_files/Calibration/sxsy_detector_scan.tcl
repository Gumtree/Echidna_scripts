drive msd 2500
drive sc 0
sampledescription "mtth120-noPC-noSC-stick"
sampletitle ""
samplename "Fe"
user "Max Avdeev"
title "Calibration"

for {set i -20} {$i <= 20} {incr i 5} {
drive sx [expr $i]
runscan sy -20 20 9 time 20 savetype save datatype HISTOGRAM_X force true
}
