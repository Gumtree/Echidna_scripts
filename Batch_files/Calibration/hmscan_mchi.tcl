proc doit {} {
	hmscan clear
        user "max"
        sample "NAC mchi scanning"
	hmscan add stth 160.75 0.05
   drive mchi 88
        hmscan run 25 timer 250
   drive mchi 89
        hmscan run 25 timer 250
   drive mchi 91
        hmscan run 25 timer 250
   drive mchi 92
        hmscan run 25 timer 250
        hmscan run 25 timer 250
}

doit
