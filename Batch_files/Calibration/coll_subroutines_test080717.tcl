gumput 1
proc SimpleCollRun {numsteps} {
gumput 2
histmem stop
gumput 3
hmm configure fat_multiple_datasets disable
gumput 4
histmem loadconf
gumput 5
histmem mode unlimited
gumput 6
som speed 0.2
gumput 7
drive som -1
gumput 8
som maxretry 0
gumput 9
som speed 0.036
gumput 10
newfile HISTOGRAM_XY scratch
gumput 11
histmem start
gumput 12
for {set i 0} {$i <$numsteps} {incr i} {
gumput 13
drive som -0.5
gumput 14
drive som -1
gumput 15
}
gumput 16
histmem pause
gumput 17
save
gumput 18
histmem stop
gumput 19
hmm configure fat_multiple_datasets enable
gumput 20
histmem loadconf
gumput 21
wait 5
gumput 22
som speed 0.2
gumput 23
}
gumput 24

gumput 25
proc CollFlatScan {motor start step numsteps} {
gumput 26
histmem stop
gumput 27
hmm configure fat_multiple_datasets disable
gumput 28
histmem loadconf
gumput 29
wait 5
gumput 30
histmem mode unlimited
gumput 31
som speed 0.2
gumput 32
drive som -1
gumput 33
som speed 0.036
gumput 34
newfile HISTOGRAM_XY scratch
gumput 35
for {set i 0} {$i <$numsteps} {incr i} {
gumput 36
drive $motor [expr $i*$step+$start]
gumput 37
histmem start
gumput 38
run som 1
gumput 39
wait 62
gumput 40
run som -1
gumput 41
wait 62
gumput 42
histmem pause
gumput 43
wait 5
gumput 44
}
gumput 45
save
gumput 46
histmem stop
gumput 47
wait 5
gumput 48
hmm configure fat_multiple_datasets enable
gumput 49
histmem loadconf
gumput 50
wait 5
gumput 51
som speed 0.2
gumput 52
}
gumput 53
title testradcoll
gumput 54
SimpleCollRun 1
gumput 55

gumput 56

