# Put sample in beam, not vacuum
title P2618
user William Brant
sampledescription mtth140-noPC-SC10-Ge335-Air
#
hset /sample/robby/control/target_loc BEAM
hset /sample/robby/control/pallet_nam B
#
proc runsamples {} {
	set pallet_list [list 8 10]
	set name_list [list {K2-xTi8O16} {TiO2_H}]
	foreach location $pallet_list a_name $name_list {
		samplename $a_name
		hset /sample/robby/control/pallet_idx $location
                drive robby_driveable 1
		broadcast $a_name
		runscan stth 2.75 5.2 50 time 419
		drive robby_driveable 0
	}
}
#
runsamples
}
