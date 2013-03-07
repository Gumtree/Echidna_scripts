# Wait for base temperature, then run
samplename NaTFSA while cooling
runscan stth 4.0 5.2 25 time 118
drive tc1_driveable2 10
samplename NaTFSA at base
runscan stth 2.75 5.2 50 time 550