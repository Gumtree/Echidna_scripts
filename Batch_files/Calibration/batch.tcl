sample "vanadiummtth90noPC"
user "max"
phone "x9522"
hmscan clear
hmscan add stth 5.75 0.025
for {set i 0} {$i < 10} {incr i} {
        hmscan run 50 monitor 12000
}
