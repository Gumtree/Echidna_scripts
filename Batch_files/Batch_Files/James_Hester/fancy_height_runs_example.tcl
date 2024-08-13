# We are using a custom command 'samp_to_vert loc ht' where loc is the
# pallet/hole and ht is the sample height in millimetres. The SampInBeam
# point on the robot should be 80mm for this to work properly

set locs { B45 B46 B47 B48}
set hts { 15 10 15 15}
set names { JZ271 JZ272 JZ273 JZ274}
set times { 527 527 527 527}

foreach location $locs height $hts sname $names counttime $times {
	samp_to_vert $location $height
	samplename $sname
	runscan stth 2.65 5.025 20 time $counttime
	old_samp_from_vac
}