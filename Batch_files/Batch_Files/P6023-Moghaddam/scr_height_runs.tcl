# We are using a custom command 'samp_to_vert loc ht' where loc is the
# pallet/hole and ht is the sample height in millimetres. The SampInBeam
# point on the robot should be 80mm for this to work properly

set locs {B31 B32 B33}
set hts {26 20 18}
set names {SS316_0pct SS316_20pct SS316_30pct}

foreach location $locs height $hts sname $names {
    samp_to_vert $location $height
    hset /sample/robby/control/rotate 1
    samplename $sname
    runscan stth 2.75 5.2 50 time 347
    hset /sample/robby/control/rotate 0
    wait 100
    old_samp_from_vac
}