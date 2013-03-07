for {set j 88.7} {$j <= 91.3}  {incr j} {
drive mchi [expr $j]
runscan stth 4 5.225 50 time 60
}
