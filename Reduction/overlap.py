# These routines calculate an Echidna tube gain correction based on overlapping tube measurements.

"""
The treatment follows the paper of Monahan, Schriffer and Schriffer in Acta Cryst, 1967 p 322.
"""
from gumpy.nexus import *

# In find_gain, we do not want to use datapoints that are zero.  We have to mask these out
def find_gain(data, variance, steps_per_tube, gain_array,pixel_mask=None,errors=False):
   import math,time
   """usage: data is a 2D gumpy Array consisting of vertically-integrated scans from multiple tubes on Echidna, 
      where successive scans start overlapping neighbouring tubes after steps_per_tube steps. 
      Variance is the corresponding variance.
      To avoid duplication of calculations, the corrected data corresponding to
      the input gain is returned as well as the new gain.  
      Pixel mask is a data-shaped array containing 0s in those positions
      where the pixel information should not be used.  If None, all pixels are used.
      If errors is True, errors are calculated"""
   if pixel_mask is None:
       pixel_mask = array.ones_like(data[0])
   elapsed = time.clock()
   print 'In find_gain: started at %f' % elapsed
   outdata,weighted_data,my_variance = apply_gain(data,variance,steps_per_tube,gain_array,pixel_mask)
   print 'Applied initial gain: %f' % (time.clock() - elapsed)
   #
   # for each observation, residual is the (observation - pixel gain * the model intensity)^2/sigma^2
   #
   residual_map = shift_sub_tube_mult_new(gain_array,outdata,data,steps_per_tube,pixel_mask)/my_variance
   print 'New residual at %f' % (time.clock() - elapsed)
   #chisquared = sum(residual_map)/(residual_map.size - gain_array.shape[-1])
   # following statistic is for statistical inference - normal distribution z value for large
   # degrees of freedom can be obtained from (chi squared - dof)/sqrt(2 dof)
   dof = residual_map.size - gain_array.shape[-1]
   norm_chi = (residual_map.sum() - dof)/math.sqrt(2.0*dof)
   print 'Chi %s at %f' % (`norm_chi`,(time.clock() - elapsed))
   # if True in isnan(outdata): raise ValueError, "NaN found!"
   # calculate our next round of scales (Eq (2) in paper)
   summed_data = shift_mult_tube_add_new(weighted_data,outdata,steps_per_tube,pixel_mask)
   summed_denominator = shift_mult_tube_add_new(1.0/my_variance,outdata,steps_per_tube,pixel_mask,squareit=True)
   # clip the denominator
   print 'Summed everything at %f ' % (time.clock() - elapsed)
   summed_denominator[summed_denominator<1e-10]=1e-10
   gain =  summed_data/summed_denominator
   print 'Gain at %f' % (time.clock() - elapsed)
   # calculate the error in each gain  from the rms differences
   if errors:
       esds = calc_error_new(data,outdata,gain,steps_per_tube,pixel_mask)
       print 'Final errors at %f' % (time.clock() - elapsed)
   else: esds = array.zeros_like(gain)
   return gain,outdata,norm_chi,residual_map,esds

def timeit(relativeto,message):
   import time
   print message + `time.clock()-relativeto`

def apply_gain(full_ds,full_variance,steps_per_tube,gain_array,pixel_mask=None):
   """ This utility routine applies the result of the find_gain routine to the full data,
   to obtain the best estimate of the actual intensities.  We have a separate routine
   as we may work with summed data during iteration"""
   import time
   elapsed = time.clock()
   if pixel_mask is None:
       pixel_mask = array.ones_like(full_ds[0])
   #sanitise - we don't like zeros or complicated datastructures
   full_data = full_ds.storage
   my_variance = copy(full_variance.storage)
   my_variance[my_variance<1.0] = 1.0
   #weighted_data = divide(full_data,my_variance)  #wd = (F_hl^2/sigma_hl^2)
   weighted_data = full_data/my_variance  #wd = (F_hl^2/sigma_hl^2) 
   trans_gain = gain_array.reshape([len(gain_array),1])
   #scaled_data = multiply(trans_gain,weighted_data)  #G_l(rho-1)*wd ; should broadcast to all scans
   # gumpy doesn't have broadcasting, so...
   scaled_data = zeros_like(weighted_data)
   for section in range(weighted_data.shape[-1]):
       scaled_data[:,section] = trans_gain*weighted_data[:,section]  #G_l(rho-1)*wd
   timeit(elapsed,'Finished doing gain multiplication')
   summed_data = shift_tube_add_new(scaled_data,steps_per_tube,pixel_mask) # Sum_l[previous line]
   timeit(elapsed,'Finished adding tubes together')
   # if True in isnan(summed_data): raise ValueError,"NaN found!"
   scaled_variance = zeros_like(my_variance)
   for section in range(my_variance.shape[-1]):
      scaled_variance[:,section] = trans_gain**2/my_variance[:,section]
   timeit(elapsed,'Finished scaling variance')
   # if True in isnan(scaled_variance): raise ValueError,"NaN found!"
   summed_denominator = shift_tube_add_new(scaled_variance,steps_per_tube,pixel_mask)
   timeit(elapsed,'Finished adding variance')
   if 0 in summed_denominator:
          if pixel_mask is None: 
              print "Warning: 0 found in summed denominator"
              print "New minimum is %g" % summed_denominator.min()
          summed_denominator[summed_denominator<1e-10] = 1e-10
          timeit(elapsed,'Finished clipping denominator')
          #clip(summed_denominator,1e-10,summed_denominator.max(),summed_denominator) 
   outdata = summed_data/summed_denominator #F_h^2 in original paper
   return outdata,weighted_data,my_variance

def shift_add(inarray,offset,pixel_mask,average=False):
    """Return the sum of the 2D slices in inarray, with each slice shifted by offset pixels
       relative to the previous slice.  The array returned contains only the subset of pixels
       where all inarray pixels contribute to the sum.  A positive offset means that 
       pixel (i,j) in the n+1th slice is added to pixel (i-*offset,j) in the nth slice.
       This corresponds to the Wombat detector scanning in positive 2th direction. Note that
       offset becomes the steps per tube value for Echidna. The result
       array is expanded by offset*noslices.Note that this means only positive offsets make sense.
       If pixel_mask is set, it will have a 1 for pixel positions that are valid, and 0 otherwise.
       if average is true, the result will be divided by the number of contributions"""
    oldshape = list(inarray[0].shape)
    newshape = copy(oldshape)
    newshape[1] = newshape[1]+offset*(len(inarray)-1)
    result = zeros(newshape)
    for asliceno in range(len(inarray)):
        result[:,offset*asliceno:oldshape[1]+offset*asliceno] += (inarray[asliceno]*pixel_mask) 
    return result

def shift_tube_add(inarray,tube_offset,pixel_mask,average=False):
    """Return the sum of the 1D slices in inarray, with each slice shifted by tube_offset 
       scan steps relative to the previous tube.  All steps with contributions from
       more than one detector are included. A positive tube_offset means that 
       step i in the n+1th slice is added to pixel (i-tube_offset) in the nth slice.
       This corresponds to the detector scanning in positive 2th direction. The result
       array is expanded by offset*notubes.Note that this means only positive offsets make sense.
       If pixel_mask is set, it will have a 1 for pixel positions that are valid, and 0 otherwise"""

    # We imagine that we have no_tubes slices of data which we want to overlap, shifting each time
    # by steps_per_tube.  The total length will be no more than (no_tubes + 1) * no_steps
    no_steps = len(inarray[0])    #store for efficiency
    newshape = [len(inarray)*tube_offset + no_steps]
    result = zeros(newshape)
    contribs = zeros(newshape)
    # Add the arrays
    for atubeno in range(len(inarray)):
        result[tube_offset*atubeno:no_steps+tube_offset*atubeno] += inarray[atubeno] 
        if average:
            contribs[tube_offset*atubeno:no_steps+tube_offset*atubeno] += ones_like(inarray[atubeno]) 
    if average:
        result = result/contribs
    return result

def shift_tube_add_new(inarray,tube_offset,pixel_mask,average=False):
    """Return the sum of the 1D slices in inarray, with each slice shifted by tube_offset 
       scan steps relative to the previous tube.  All steps with contributions from
       more than one detector are included. A positive tube_offset means that 
       step i in the n+1th slice is added to pixel (i-tube_offset) in the nth slice.
       This corresponds to the detector scanning in positive 2th direction. The result
       array is expanded by offset*notubes.Note that this means only positive offsets make sense.
       If pixel_mask is set, it will have a 1 for pixel positions that are valid, and 0 otherwise.
       This new version avoids using Jython slice notation due to the slowdown caused by the
       gumpy __getitem__ and __setitem__ methods."""

    # We imagine that we have no_tubes slices of data which we want to overlap, shifting each time
    # by steps_per_tube.  The total length will be no more than (no_tubes + 1) * no_steps
    no_steps = len(inarray[0])    #store for efficiency
    newshape = [len(inarray)*tube_offset + no_steps]
    oldshape = inarray.shape
    working_data = inarray.storage   #for speed
    result = array.zeros(newshape)
    contribs = array.zeros(newshape)
    slice_iter = working_data.__iter__()
    # Add the arrays
    for atubeno in range(len(inarray)):
        rta = result.get_section([atubeno*tube_offset],[oldshape[1]])
        rta += slice_iter.next()
    return result

def shift_mult_add(fixed_array, sliding_array,offset, pixel_mask,squareit = False):
    """This is in some sense the inverse of the shift_add routine.  Fixed array is a
       set of detector images, and sliding_array is a single map of intensity values
       produced by the shift_add routine. We multiply the two
       arrays, shifting sliding array by offset each time it is multiplied by a layer
       of fixed_array.  Pixels in sliding array
       that are beyond the end of fixed_array are ignored. If squareit is true,
       the result of the multiplication is squared before summing."""
    result = zeros_like(fixed_array[0])
    tthlen = result.shape[1]
    numslices = len(fixed_array)   #for convenience
    if not squareit:
        for asliceno in range(numslices):
            result = result + (fixed_array[asliceno]*pixel_mask)*(sliding_array[:,offset*asliceno:tthlen + offset*asliceno])
    else:
        for asliceno in range(numslices):
            result = result + (fixed_array[asliceno]*pixel_mask)*(sliding_array[:,offset*asliceno:tthlen + offset*asliceno])**2
    return result

def shift_mult_tube_add(fixed_array, sliding_vector,tube_offset, pixel_mask,squareit = False):
    """This is in some sense the inverse of the shift_add routine.  Fixed array is a
       set of tube scans, and sliding_array is a single line of intensity values
       produced by the shift_tube_add routine. We multiply the two
       vectors, shifting sliding vector by offset each time it is multiplied by a section 
       of fixed_array.  Points in sliding vector 
       that are beyond the end of fixed_array are ignored. If squareit is true,
       the result of the multiplication is squared before summing.  The result
       will be a vector with length corresponding to the number of tubes"""
    result = zeros(len(fixed_array))  #one value per tube
    scanlen = len(fixed_array[0])  #number of steps per tube
    numslices = len(fixed_array)   #for convenience
    if not squareit:
        for atubeno in range(numslices):
            result[atubeno] = sum((fixed_array[atubeno]*pixel_mask)*(sliding_vector[tube_offset*atubeno:scanlen + tube_offset*atubeno]))
            if atubeno == 64:
               sv = sliding_vector[tube_offset*atubeno:scanlen + tube_offset*atubeno]
               print 'obi,sv,rta: ' + `fixed_array[atubeno]` + '\n' + `sv` + '\n' + `result[atubeno]`
    else:
        for atubeno in range(numslices):
            result[atubeno] = sum((fixed_array[atubeno]*pixel_mask)*(sliding_vector[tube_offset*atubeno:scanlen + tube_offset*atubeno]**2))
            if atubeno == 64:
               sv = sliding_vector[tube_offset*atubeno:scanlen + tube_offset*atubeno]
               print 'obi,sv,rta: ' + `fixed_array[atubeno]` + '\n' + `sv` + '\n' + `result[atubeno]`
    return result

def shift_mult_tube_add_new(fixed_array, sliding_vector,tube_offset, pixel_mask,squareit = False):
    """This is in some sense the inverse of the shift_add routine.  Fixed array is a
       set of tube scans, and sliding_array is a single line of intensity values
       produced by the shift_tube_add routine. We multiply the two
       vectors, shifting sliding vector by offset each time it is multiplied by a section 
       of fixed_array.  Points in sliding vector 
       that are beyond the end of fixed_array are ignored. If squareit is true,
       the result of the multiplication is squared before summing.  The result
       will be a vector with length corresponding to the number of tubes. The
       'new' suffix means it has been optimised for gumpy."""
    result = array.zeros(len(fixed_array))  #one value per tube
    scanlen = len(fixed_array[0])  #number of steps per tube
    numslices = len(fixed_array)   #for convenience
    try:
       working_obs = fixed_array.storage
    except AttributeError:
       working_obs = fixed_array   #already an Array
    obs_i = working_obs.__iter__() #for speed
    rti = result.__iter__()
    if not squareit:
        for atubeno in range(numslices):
            sv = sliding_vector.get_section([tube_offset*atubeno],[scanlen])
            obi = obs_i.next()
            rti.set_next(sum((obi*pixel_mask)*sv))
    else:
        for atubeno in range(numslices):
            sv = sliding_vector.get_section([tube_offset*atubeno],[scanlen])
            obi = obs_i.next()
            rti.set_next(sum((obi*pixel_mask)*sv**2))
    return result

def shift_sub_mult(gain_array,model_array,obs_array,offset,pixel_mask):
    """This performs the operation of obs_array - gain*model.  Depending on the
       slice of obs_array, the gain and model relative placements are chosen"""
    result = zeros_like(obs_array)
    tthlen = obs_array.shape[2]
    numslices = len(obs_array)   #for convenience
    for asliceno in range(numslices):
        result[asliceno] = square(obs_array[asliceno]*pixel_mask - gain_array*model_array[:,offset*asliceno:tthlen + offset*asliceno])
    return result
       
def shift_sub_tube_mult(gain_vector,model_vector,obs_array,offset,pixel_mask):
    """This performs the operation of obs_array - gain*model.  Depending on the
       slice of obs_array, the gain and model relative placements are chosen"""
    result = zeros_like(obs_array)
    scanlen = obs_array.shape[1]
    numslices = len(obs_array)   #for convenience
    for atubeno in range(numslices):
        result[atubeno] = (obs_array[atubeno]*pixel_mask - gain_vector[atubeno]*model_vector[offset*atubeno:scanlen + offset*atubeno])**2
    return result
       
def shift_sub_tube_mult_new(gain_vector,model_vector,obs_array,offset,pixel_mask):
    """This performs the operation of obs_array - gain*model.  Depending on the
       slice of obs_array, the gain and model relative placements are chosen. 
       Optimised for speed on gumpy."""
    result = array.zeros_like(obs_array)
    scanlen = obs_array.shape[1]
    numslices = len(obs_array)   #for convenience
    working_obs = obs_array.storage
    obs_i = working_obs.__iter__() #for speed
    gv_iter = gain_vector.__iter__() # for speed
    #print 'Result shape: ' + `result.shape`
    for atubeno in range(numslices):
        rta = result.get_section([atubeno,0],[1,scanlen])
        obi = obs_i.next()
        gvi = gv_iter.next()
        model_sec = model_vector.get_section([atubeno*offset],[scanlen])
        # if atubeno == 64:
        #    print 'mask, obi,gvi ' + `pixel_mask` + `gvi` + ' ' + `obi` + ' ' + `model_sec`
        rta += (obi*pixel_mask - gvi*model_sec)**2
        #if atubeno == 64:
        #    print 'rta ' + `rta`
    #print 'Result [64,1] = ' + `result[64][1]`
    return result
       
def shift_apply_gain_add(gain_vector,model_vector,offset,total_steps):
    """Apply the gain to the model vector to produce the model intensity for this point, and sum all
       values obtained.  Offset is the distance in steps between tubes, and total_steps is the
       total number of steps each tube takes."""
    sum = 0.0
    numtubes = len(gain_vector)
    for atube in range(numtubes):
        sum += gain[atube]*model_vector[atube*offset:atube*offset+total_steps]
    return sum
     
# This function calculates the error in the gain numbers by getting the RMS deviation of obs_point/model_point
def calc_error(obs,model,gain_vector,offset,pixel_mask):
    # We should calculate  as for shift_sub_tube_mult, but dividing instead
    import math
    result = zeros_like(gain_vector)
    scanlen = obs.shape[1]
    numslices = len(obs)
    for atubeno in range(numslices):
        result[atubeno] = math.sqrt(sum((gain_vector[atubeno]-(obs[atubeno]*pixel_mask/model[offset*atubeno:scanlen + offset*atubeno]))**2)/scanlen)
    return result

# This function calculates the error in the gain numbers by getting the RMS deviation of obs_point/model_point
def calc_error_new(obs,model,gain_vector,offset,pixel_mask):
    # We should calculate  as for shift_sub_tube_mult, but dividing instead
    import math
    result = array.zeros_like(gain_vector)
    ri = result.__iter__()
    gi = gain_vector.__iter__()
    oi = obs.storage.__iter__()
    scanlen = obs.shape[1]
    numslices = len(obs)
    for atubeno in range(numslices):
        rta = ri.next()
        mod_sec = model.get_section([offset*atubeno],[scanlen])
        rta += math.sqrt(sum((gi.next()-(oi.next()*pixel_mask/mod_sec))**2)/scanlen)
    return result

# Thus function performs linear interpolation on the input array to calculate intermediate values.
# The meaning of the shift is that the routine should calculate the values for dataset if the
# values as provided correspond to angular values shift_ang lower than the return values
def apply_shift(dataset,ang_step,shift_ang):
    shift_prop = shift_ang/ang_step
    shifted_vals = zeros_like(dataset)
    dataset_b = dataset[1:]
    diffarray = dataset_b - dataset[:-1]
    if shift_prop > 0:          # we are shifting forward
        shifted_vals[:-1] = (shift_prop * diffarray) + dataset[:-1]
        shifted_vals[-1] = (shift_prop+1)*diffarray[-1] + dataset[-1]  #final value
    else:                       # we are shifting back
        shifted_vals[1:] = (shift_prop * diffarray) + dataset[1:]
        shifted_vals[0] = (shift_prop-1)*diffarray[0] + dataset[0]  #final value
    print "Shifted by %f: max intensity shift %f" % (shift_ang,max(shift_prop*diffarray))
    return shifted_vals 

def output_result(results,filename="smoothing_result.txt",start_angle=15):
    """Write a simple results file in two columns"""
    ofile = open(filename,"w")
    ofile.write("#Results of attempting a Wombat gain calculation using overlapping detector scans\n")
    for point in range(len(results)):
        ofile.write("%8.4f %8.4f\n" % (point*0.125 + start_angle,results[point]))

def iterate_gain(data,variance,pixel_step,epsilon=0.001):
    """Calculate a gain array by iteration until the change in all points is less than a predetermined value"""
    start_gain = array.ones_like(data[0])
    print "Data shape: " + `data.shape`
    gain,first_ave,last_c,r = find_gain(data,variance,pixel_step,start_gain)
    gain,next_ave,c,r = find_gain(data,variance,pixel_step,gain)
    #difference = absolute(next_ave/(next_ave - first_ave))
    difference = last_c - c
    last_c = c 
    cycle_count = 0
    while difference > epsilon:
        cycle_count+=1
        gain,next_ave,c,residual_map = find_gain(data,variance,pixel_step,gain)
        #difference = absolute(next_ave/(next_ave - last_ave))
        print "Cycle %d: Chi squared %f, shift %f" % (cycle_count,c, last_c - c)
        difference = last_c - c
        last_c = c
    return gain,next_ave,difference,cycle_count,residual_map
        
     
