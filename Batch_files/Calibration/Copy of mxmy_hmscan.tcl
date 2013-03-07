for {set j -12} {$j <= 12} {incr j 6} {
drive my [expr $j]
runscan stth 4 5.225 50 time 60
}
