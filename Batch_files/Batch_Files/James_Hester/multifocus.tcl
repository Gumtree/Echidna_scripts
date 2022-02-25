# Run the monochromator at different foci to see if there is an effect on
# resolution. 

foreach foc { 0.30 0.25 0.15 0.1 0.0 } {
	drive mf1 $foc
	samplename [ concat rocking curve at focus $foc ] 
	runscan mom 69.0 71.0 21 time 60 
}