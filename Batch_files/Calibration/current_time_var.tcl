# Add the following VarMake to extraconfig.tcl 
# VarMake currtime text user

clientput Hi there
currtime [sicstime]
clientput [currtime]
set currsec [clock seconds]
wait 10
clientput [sicstime]
clientput [expr [clock seconds] - $currsec]
