# ZFC scan
samplename Fe3O4 nanoballs at base temperature
runscan stth 1.5 5.2 75 time 214
# Apply 1T field
samplename ZFC Fe3O4 nanoballs in 1T field
magnet send s 1.0
wait 300
runscan stth 1.5 5.2 75 time 214
# Now heat
drive tc2 200
samplename Fe3O4 at 200K after heating in 1T field
runscan stth 2.75 5.2 25 time 61
# Now cool again
drive tc2 6
# switch off heater
hset /sample/tc2/heater/heaterRange 0
samplename Fe3O4 approaching base after cooling in 1T field
runscan stth 2.75 5.2 25 time 61
# Now collect at base for real
magnet send s 0
wait 300
samplename Fe3O4 at base, 0 Tesla after cooling in 1T field
runscan stth 1.5 5.2 75 time 214

