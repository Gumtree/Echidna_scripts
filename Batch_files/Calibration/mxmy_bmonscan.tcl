for {set i -12} {$i <= 12} {incr i 4} {
drive mx [expr $i] 
bmonscan clear   
bmonscan add my -12 4
bmonscan run 7 timer 30
}
