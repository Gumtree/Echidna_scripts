# Collect a series of samples in the beam
hset /sample/robby/control/target_loc BEAM

proc do_multisamples {} {
	set poslist [list 26 28 30 ]
	set namelist [list {samp1} {samp2} {samp3} ]
	set timelist [list 131 131 131 ]
	foreach samp_name $namelist exp_time $timelist samp_pos $poslist {
		samplename $samp_name
		hset /sample/robby/control/pallet_idx $samp_pos
		drive robby_driveable 1
		runscan stth 2.75 5.2 50 time $exp_time
		drive robby_driveable 0
	}
}

do_multisamples