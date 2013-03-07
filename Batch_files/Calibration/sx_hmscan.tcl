drive msd 2500
drive sc 0
sampledescription ""
#---------------
sampletitle "Calibration"
#---------------
user "Max Avdeev"
title "Scanning pcr"

newfile HISTOGRAM_XY
histmem mode time
histmem preset 60

set k 177.4;
set index 0;

while {$k <=179} {
drive pcr [expr $k]
set k [expr $k+0.2]
histmem start block
save $index
set index [expr $index+1]
}
