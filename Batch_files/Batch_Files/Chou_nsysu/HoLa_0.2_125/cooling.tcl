title Proposal 654
sampledescription mtth140-noPC-noSC-TopLoader-Ge335
user H. Chou
sampletitle HoLa-0.2_125

#
#tc2 tolerance 100
#tc2 controlsensor sensorA
#tc2 range 5
#tc2 heateron 0
#

tc2 heateron 1
hset /sample/tc1/heater/heaterRange_1 3
hset /sample/tc1/heater/heaterRange_2 3


samplename HoLa-0.2_125 cooling-4k
runscan stth 4.0 5.2 25 time 118
