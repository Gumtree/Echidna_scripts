# Collect a series of samples in the beam
hset /sample/robby/control/target_loc BEAM

proc do_multisamples {} {
	set poslist [list 28 30 24 10 10 22 ]
	set namelist [list {#34 CaD2-2} {#35 CaD2-3} {#16 La033Sr05TiO3 red afterwash} {#15 La033Sr05TiO3 red beforewash} {#15 La033Sr05TiO3 red beforewash} {#9 Sr2TiO3F} ]
	set timelist [list 95 95 131 131 131 131 ]
	foreach samp_name $namelist exp_time $timelist samp_pos $poslist {
		samplename $samp_name
		hset /sample/robby/control/pallet_idx $samp_pos
		drive robby_driveable 1
		runscan stth 2.75 5.2 50 time $exp_time
		drive robby_driveable 0
	}
}

do_multisamples