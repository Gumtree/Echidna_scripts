drive msd 2500
drive sc 1
#---------------
sampletitle "Calibration"
#---------------
user "Vanessa Peterson"
title "Scanning scr P1241"

newfile HISTOGRAM_XY
histmem mode time
histmem preset 90

set k 0;
set index 0;

while {$k <=0.7} {
drive scr [expr $k]
set k [expr $k+0.1]
histmem start block
save $index
set index [expr $index+1]
}
