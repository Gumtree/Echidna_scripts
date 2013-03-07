title Proposal 1045
sampledescription mtth140-noPC-noSC-Ge335
user Jyotish Debnath
#
# Sequence of temperatures using bottom loader and Lakeshore 336
#
#
#  Next temperature
#
# Cooling down
set testbit 0
samplename La0.7Ca0.3Co03 cooling in $testbit T field
runscan stth 4.0 5.2 25 time 118
runscan stth 4.0 5.2 25 time 118
#
#
# apply a magnetic fields
#
set fieldlist {1.0 0.0}

set st 0
foreach field $fieldlist {
  magnet send s [expr {$field*2}]
  set wt [expr {(($field*2) - $st)*100 + 5 }]
  wait $wt
  samplename La0.7Ca0.3Co03 at base, B= $field
  runscan stth 4.0 5.2 25 time 406
  set st $field
  }
magnet send s 0
wait 900
#
# switch on heating
hset /sample/tc1/heater/heaterRange_1 3
drive tc1_driveable 150
wait 900
# switch off heating, switch on field, wait for cooling
magnet send s 3.0
wait 300
hset /sample/tc1/heater/heaterRange_1 0
samplename La0.7Ca0.3Co03 cooling in 1.5T field
runscan stth 4.0 5.2 25 time 118
runscan stth 4.0 5.2 25 time 118
#
magnet send s 0
wait 300
set st 0
foreach field fieldlist {
  magnet send s [expr {$field*2}]
  set wt [expr {(($field*2 ) - $st)*100 + 5}]
  wait $wt
  samplename La0.7Ca0.3Co03 at base after field cooling, B= $field
  runscan stth 4.0 5.2 25 time 406
  set st $field
  }
magnet send s 0