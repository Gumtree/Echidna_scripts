sample "background_mtth90_noPC_stth7"
user "max"
phone "x9522"
email "max@ansto.gov.au"

for {set i 0} {$i < 10} {incr i} 

{
::histogram_memory::count_bm_controlled timer 10
::histogram_memory::save
}
