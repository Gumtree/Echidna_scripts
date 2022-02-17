# We are using a custom command 'samp_to_vert loc ht' where loc is the
# pallet/hole and ht is the sample height in millimetres. The SampInBeam
# point on the robot should be 80mm for this to work properly

set locs {B35 B36 }
set hts {20 14 }
set names {SC24 SC16 }
set times { 419 419 }

foreach location $locs height $hts sname $names counttime $times {
	samp_to_vert $location $height
	samplename $sname
	runscan stth 2.75 5.225 100 time $counttime
	old_samp_from_vac
}

samplename Pbtest
samp_to_vert B37 50
runscan stth 2.75 5.2 50 time 275
old_samp_from_vac
