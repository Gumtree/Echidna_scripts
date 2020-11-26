# These routines calculate an Echidna tube gain correction based on overlapping tube measurements.

"""
Routines appended with '_fr_' for routines derived from 
Fox and Rollet, Acta Cryst. B24, p293(1968).
"""
from copy import copy
from gumpy.nexus import *

def timeit(relativeto,message):
   import time
   print message + `time.clock()-relativeto`

def apply_gain(full_ds,weights,gain_array,calc_var=False,pixel_mask=None,bad_steps=[]):
   """ This utility routine applies the result of the find_gain_fr routine to the full data,
   to obtain the best estimate of the actual intensities. If calc_var is true, the
   variance of the estimate is calculated as well. Bad steps are assumed to have
   been zeroed previously. Data has the dimensions n tubes x m sections x p steps"""
   import time
   elapsed = time.clock()
   if pixel_mask is None:
       pixel_mask = array.ones_like(full_ds)
   #sanitise - we don't like zeros or complicated datastructures
   full_data = full_ds.storage
   my_weights = copy(weights)
   try:
      my_weights = my_weights.storage
   except AttributeError:
      pass
   if calc_var is True:  #we assume variance is 1/weights for esd calcs
      my_variance = 1.0/my_weights  #we are assuming that 1.0/0 = 0 for excluded bits
   #weighted_data = divide(full_data,my_variance)  #wd = (F_hl^2/sigma_hl^2)
   weighted_data = full_data*my_weights  #wd = (F_hl^2/sigma_hl^2)
   # create a gain array with the same shape as the data
   trans_gain = zeros_like(weighted_data)
   for tubeno in range(weighted_data.shape[0]):   #loop over tubes
      trans_gain[tubeno] = gain_array[tubeno]
   # trans_gain = gain_array.reshape([len(gain_array),1])
   #scaled_data = multiply(trans_gain,weighted_data)  #G_l(rho-1)*wd ; should broadcast to all scans
   # gumpy doesn't have broadcasting, so...
   scaled_data = zeros_like(weighted_data)
   #for section in range(weighted_data.shape[-1]):
   scaled_data = trans_gain*weighted_data  #G_l(rho-1)*wd
   summed_data = shift_tube_add_new(scaled_data,pixel_mask) # Sum_l[previous line]
   scaled_weights = zeros_like(my_weights)
   scaled_weights = trans_gain**2*my_weights
   # if True in isnan(scaled_variance): raise ValueError,"NaN found!"
   summed_denominator = shift_tube_add_new(scaled_weights,pixel_mask)
   if 0 in summed_denominator:
          if pixel_mask is None: 
              print "Warning: 0 found in summed denominator"
              print "New minimum is %g" % summed_denominator.min()
          summed_denominator[summed_denominator<1e-10] = 1e-10
          #clip(summed_denominator,1e-10,summed_denominator.max(),summed_denominator) 
   outdata = summed_data/summed_denominator #F_h^2 in original paper
   # Get a proper error for observations
   if calc_var is True:
      # Until we get matrix inversion, we estimate the errors as being simply that obtained
      # assuming no error in the gain, in which case assuming gains approx 1 and intensities
      # similar to one another, sigma^2(F_h) = sum_p(sigma^2(F_hp))/N^2
      final_variances = shift_tube_add_new(my_variance,pixel_mask)
      contributor_count = shift_tube_add_new(ones_like(my_variance),pixel_mask)
      final_variances = final_variances/(contributor_count**2)
      # esds on gain are set at 0.01 pending matrix inversion
      esds = calc_error_rough(gain_array)
   else:
      final_variances = zeros_like(outdata)
      esds = zeros_like(gain_array)
   return outdata,weighted_data,final_variances,esds

def shift_tube_add_new(inarray,pixel_mask,average=False):
    """Sum the 1D slices in inarray, which is an array of dimensions n tubes x 
       m sections x p steps.  Each section is added to the total 1D array at position
       (n+m)*p.
       If pixel_mask is set, it will have a 1 for pixel positions that are valid, and 0 otherwise.
       This new version avoids using Jython slice notation due to the slowdown caused by the
       gumpy __getitem__ and __setitem__ methods."""

    # We imagine that we have no_tubes slices of data which we want to overlap, shifting each time
    # by steps_per_tube.  The total length will be no_tubes* no_steps + offset
    tube_offset = inarray.shape[-1]  #number of steps in an angular section
    no_steps = inarray.shape[1]*inarray.shape[2]    #total steps per tube
    # The final tube covers an extra (no_steps - tube_offset) points compared to non-overlapping scans
    newshape = [len(inarray)*tube_offset + no_steps - tube_offset]
    oldshape = inarray.shape
    try:
       working_data = inarray.storage   #for speed
    except AttributeError:              #already an array
       working_data = inarray
    result = array.zeros(newshape)
    contribs = array.zeros(newshape)
    slice_iter = working_data.__iter__()
    # Add the arrays
    for atubeno in range(len(inarray)):
        rta = result.get_section([atubeno*tube_offset],[oldshape[1]*oldshape[2]])
        rtan = slice_iter.next()
        rta += rtan.flatten()
    return result

def shift_mult_fr_add(gain_array,model_array,obs_array,weight_array,pixel_mask):
   """ Perform the summation in eqn 3 of Fox and Rollet """
   import time
   # Calculate the normalising factor
   # For each angle h we form the sum over tubes of G^2_(j,r-1)/var_(h,j)
   # This is the sum of all gains contributing to range h. We divide gains by
   # variance, then do a shift-sum to get the totals
   scaled_weight = array.zeros_like(weight_array)
   swlen = scaled_weight.shape[1]
   seclen = scaled_weight.shape[2]
   for tube_no in range(len(gain_array)):
      sws = scaled_weight.get_section([tube_no,0,0],[1,swlen,seclen])
      was = weight_array.get_section([tube_no,0,0],[1,swlen,seclen])
      sws += gain_array[tube_no]**2 * was
   scale_factors = shift_tube_add_new(scaled_weight,pixel_mask)
   # Now for the other terms
   a_p_array = array.zeros_like(gain_array)
   tube_steps = obs_array.shape[1]*obs_array.shape[2]   #How many steps each tube takes
   try:
      oba = obs_array.storage
   except AttributeError:
      oba = obs_array
   for tube_no in range(len(gain_array)):
      obs_section = oba[tube_no].flatten()  #F^2_{hp}
      wt_section = weight_array[tube_no].flatten() #w_{hp}
      mod_section = model_array.get_section([seclen*tube_no],[tube_steps]) #F^2_{h,r}
      a_p_array[tube_no] = (wt_section*(mod_section**2) + \
          wt_section**2 * obs_section * (obs_section - 2.0*mod_section*gain_array[tube_no]) / \
          scale_factors.get_section([seclen*tube_no],[tube_steps])).sum()
   return a_p_array

def fr_get_cpr(gain_array,model_array,obs_array,weight_array,aparray,pixel_mask):
   """Calculate Cp,r as per eqn (5) of Fox and Rollett"""
   cpr_array = array.zeros_like(gain_array)
   offset = obs_array.shape[-1]
   tube_steps = obs_array.shape[1]*obs_array.shape[2]   #How many steps each tube takes
   try:
      oba = obs_array.storage
   except AttributeError:
      oba = obs_array
   for tube_no in range(len(gain_array)):
      obs_section = oba[tube_no].flatten()  #F^2_{hp}
      wt_section = weight_array[tube_no].flatten() #w_{hp}
      mod_section = model_array.get_section([offset*tube_no],[tube_steps]) #F^2_{h,r}
      cpr_array[tube_no] = gain_array[tube_no] + (wt_section*mod_section*obs_section).sum()/aparray[tube_no] - \
          gain_array[tube_no]*(wt_section*mod_section**2).sum()/aparray[tube_no]
   return cpr_array
        
def shift_sub_tube_mult_new(gain_vector,model_vector,obs_array,pixel_mask):
    """This performs the operation of obs_array - gain*model.  Depending on the
       slice of obs_array, the gain and model relative placements are chosen. 
       Optimised for speed on gumpy."""
    result = array.zeros_like(obs_array)
    scanlen = obs_array.shape[1]*obs_array.shape[2]
    offset = obs_array.shape[2]
    numslices = len(obs_array)   #for convenience
    working_obs = obs_array.storage
    obs_i = working_obs.__iter__() #for speed
    gv_iter = gain_vector.__iter__() # for speed
    #print 'Result shape: ' + repr(result.shape)
    for atubeno in range(numslices):
        obi = obs_i.next()
        gvi = gv_iter.next()
        mss = model_vector.get_section([atubeno*offset],[scanlen])
        model_sec = mss.reshape(obi.shape)  #this works for shape [m sections, p steps]
        #if atubeno == 2:
        #    print 'Flat section tube 2' + repr(mss)
        #    print 'sstmn tube 2: obi,gvi,model ' + `obi` + ' ' + repr(gvi) + ' ' + `model_sec`
        result[atubeno] = (obi - gvi*model_sec)**2
    #print 'Result [64,1] = ' + `result[64][1]`
    return result
 
# This function calculates the error in the gain numbers by getting the RMS deviation of obs_point/model_point
# This is incorrect as the RMS deviation contains contributions from counting error as well.
def calc_error_new(obs,model,gain_vector):
    # We should calculate  as for shift_sub_tube_mult, but dividing instead
    import math
    result = array.zeros_like(gain_vector)
    ri = result.__iter__()
    gi = gain_vector.__iter__()
    oi = obs.storage.__iter__()
    scanlen = obs.shape[1]*obs.shape[2]
    offset = obs.shape[2]
    numslices = len(obs)
    for atubeno in range(numslices):
        mod_sec = model.get_section([offset*atubeno],[scanlen])
        oin = oi.next().flatten()
        ri.set_next(math.sqrt(sum((gi.next()-(oin/mod_sec))**2)/scanlen))
    return result

def calc_error_rough(gain_vector):
   """Provide a previously-calculated error for the provided gain vector"""
   result = array.ones_like(gain_vector)
   result = result * 0.01   #approximate error
   return result

# The treatment of Ford and Rollett  Acta Cryst. (1968) B24,293
# In find_gain, we do not want to use datapoints that are zero.  We have to mask these out
def find_gain_fr(data, data_weights, gain_array,arminus1=None,pixel_mask=None,errors=False,
                 accel_flag=True):
   import math,time
   """usage: data is a 3D gumpy Array consisting of vertically-integrated scans from multiple tubes on Echidna, 
      where successive scans start overlapping neighbouring tubes after steps_per_tube steps. 
      The dataset has dimensions n tubes x m sections x p steps per section.
      Variance is the corresponding variance.
      To avoid duplication of calculations, the corrected data corresponding to
      the input gain is returned as well as the new gain.  
      Pixel mask is a data-shaped array containing 0s in those positions
      where the pixel information should not be used.  If None, all pixels are used.
      If errors is True, errors are calculated.
      If accel_flag is True, the accelerated version of Ford and Rollett is used.
      """
   if pixel_mask is None:
       pixel_mask = array.ones_like(data)
   elapsed = time.clock()
   outdata,weighted_data,outdata_vars,dummy = apply_gain(data,data_weights,gain_array,pixel_mask)
   # Now calculate A_p (Equation 3 of FR)
   # Refresher: 
   # index 'h' in FR refers to a particular angle for us
   #           or alternatively, a particular angular range if we are adding first
   # index 'p' in FR refers to a particular tube for which we want the gain
   # index 'r' is the cycle number
   # index 'j' in equation (3) is a sum over tubes
   #
   aparray = shift_mult_fr_add(gain_array,outdata,data,data_weights,pixel_mask)
   cpr = fr_get_cpr(gain_array,outdata,data,data_weights,aparray,pixel_mask)
   #
   dpr = zeros_like(cpr)
   dpr[cpr>0.5*gain_array] = cpr
   dpr[cpr<=0.5*gain_array] = 0.5*gain_array
   epr = dpr/dpr[0]
   # no acceleration
   if accel_flag is False:
      gain = epr
      K = 0.0
      ar = zeros_like(gain_array)
   else:
      ir = epr-gain_array
      if arminus1 is None:
         K = 0
      else:
         K = sum(arminus1*ir)/sum(arminus1 *arminus1)
         if K>0.3: 
            K=0.3
      ar = ir/(1.0-K)
      gain = gain_array + ar
   if errors:
       esds = calc_error_new(data,outdata,gain)
   else: esds = array.zeros_like(gain)
   return gain,outdata,ar,esds,K

def get_statistics_fr(gain,outdata,data,variances,pixel_mask):
   """Calculate some refinement statistics"""
   import math
   #
   # for each observation, residual is the (observation - pixel gain * the model intensity)^2/sigma^2
   #
   if pixel_mask is None:
       pixel_mask = array.ones_like(data)
   try:
      my_variances = variances.storage
   except AttributeError:
      my_variances = variances
   steps_per_tube = data.shape[-1]
   residual_map = shift_sub_tube_mult_new(gain,outdata,data,pixel_mask)/my_variances
   #print 'Check: residual map for tube 2 (gain %f)\n ' % gain[2] + str(residual_map[2])
   #print 'Relevant model intensities: \n' + str(outdata[2*steps_per_tube:4*steps_per_tube])
   #print 'Observed intensites:\n' + str(data.storage[2])
   #print 'Check: obs %d gains %d model intensities %d' % (residual_map.size,len(gain),len(outdata))
   #print 'Check: reduction factor is ' + str(residual_map.size - len(gain)-len(outdata))
   #print 'Check: sum ' + repr(residual_map.sum())
   #print 'Check: sum for tube 2 ' + repr(residual_map[2].sum())
   #print 'Check: residual for tube 2, step 2 ' + repr(residual_map[2][0][2])
   #print 'Check: data for tube 2, entry 2 ' + repr(data.storage[2][0][2])
   #print 'Check: variance for tube 2, entry 2 ' + repr(my_variances[2][0][2])
   #print 'Check: model for tube 2, entry 2 ' + repr(outdata[2*steps_per_tube+2])
   #print 'Check: gain for tube 2 ' + repr(gain[2])
   chisquared = abs(residual_map.sum()/(residual_map.size - len(gain) - len(outdata)))
   # following statistic is for statistical inference - normal distribution z value for large
   # degrees of freedom can be obtained from (chi squared - dof)/sqrt(2 dof)
   dof = residual_map.size - gain.shape[-1]
   norm_chi = (residual_map.sum() - dof)/math.sqrt(2.0*dof)
   return chisquared,residual_map
