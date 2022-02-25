set locs { A9 A7 A30 A2 A4 }
set hts { 60 54 54 54 80 }
set names { 105 108 109 115 101 }
set times { 203 203 203 203 203 }

foreach location $locs height $hts sname $names counttime $times {
	samp_to_vert $location $height
	samplename $sname
	runscan stth 2.75 5.2 50 time $counttime
	old_samp_from_vac
}