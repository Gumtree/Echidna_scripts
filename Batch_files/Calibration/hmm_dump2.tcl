sample "GeSC"
user "max"
phone "x9522"
email "max@ansto.gov.au"

for {set i 0} {$i < 90} {incr i} {
drive som [expr $i*1]
::histogram_memory::count_bm_controlled timer 60
::histogram_memory::save $i
}
