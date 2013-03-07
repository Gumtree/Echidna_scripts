drive msd 2500
drive sc 1
sampledescription "mtth140-noPC-SC10"
hklval "335"
#---------------
sampletitle Alignment
#---------------
user Neeraj Sharma
samplename Scanning scr
newfile HISTOGRAM_XY
histmem mode time
histmem preset 61
set k  -0.1;
set index 0;
while {$k <=0.7} {
drive scr [expr $k]
set k [expr $k+0.1]
histmem start block
save $index
set index [expr $index+1]
}