set locs { A49 A47 }
set hts { 80 80 }
set names { 111 117 }
set times { 203 203 }

foreach location $locs height $hts sname $names counttime $times {
	samp_to_vert $location $height
	samplename $sname
	runscan stth 2.75 5.2 50 time $counttime
	old_samp_from_vac
}