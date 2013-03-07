newfile HISTOGRAM_XY
histmem mode time
histmem preset 50
for {set index 0; set i -5} {$i <= 5} {incr i 5} {
for {set j -5} {$j <= 5} {incr j 5; incr index} {
drive sx [expr $i] sy [expr $j]
histmem start block
save $index
#runscan stth 4 5.225 50 time 50
}
}
