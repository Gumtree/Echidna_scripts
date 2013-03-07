title Proposal 1045
sampledescription mtth140-noPC-noSC-Ge335
user Jyotish Debnath
#
# Sequence of temperatures using bottom loader and Lakeshore 336
#
#
#  Next temperature
#
  magnet send s 2.0
  wait 300
  samplename La0.7Ca0.3Co03 at base, FC, B=-1.0T
  runscan stth 4.0 5.2 25 time 406
magnet send s 0
wait 300
samplename La0.7Ca0.3Co03 at base, FC, B=0T
runscan stth 4.0 5.2 25 time 406
