# put some samples in the beam
proc runsamples {} {
	set poslist {21}
	set samplist {LiCoFe}
	hset /sample/robby/control/target_loc BEAM
	hset /sample/robby/control/pallet_nam B
	foreach pos $poslist name $samplist {
		samplename $name
		hset /sample/robby/control/pallet_idx $pos
		drive robby_driveable 1
		# runscan stth 2.75 5.2 50 time 203
		# drive robby_driveable 0
	}
}

runsamples