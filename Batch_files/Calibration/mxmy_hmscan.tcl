for {set i -12} {$i <= 12} {incr i 6} {
for {set j -12} {$j <= 12} {incr j 6} {
drive mx [expr $i] 
drive my [expr $j]
runscan stth 4 5.225 50 time 60
}
}
