stth fixed 1
set mtthstart [SplitReply [mtth]]
set mtthstop [expr $mtthstart + 10]
clientput run mtth from $mtthstart to $mtthstop
while {1} {
clientput run mtth to $mtthstop
	drive mtth $mtthstop
clientput run mtth to $mtthstart
	drive mtth $mtthstart
}
stth fixed -1
