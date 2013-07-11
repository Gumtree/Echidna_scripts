def scrub_vanad_pos(vanad,takeoff,crystal,nosteps=25):
    """Return a (tube,minstep,maxstep) list describing where
       vanadium peaks occur for these settings"""
    takeoff = int(round(takeoff))
    if crystal=='335' and takeoff==140 and nosteps==75:
       return [
              [32,50,70],   #110 at 44 degrees
              [33,25,45],
              [34,0,20],
              [48,55,75],   #200 
              [49,30,50],
              [50,5,25],
              [62,50,75],   #211
              [63,25,50],
              [64,0,25],
              [75,60,75],   #220
              [76,35,50],
              [77,10,25] 
              ]
    elif crystal=='335' and takeoff==140 and nosteps==50:
       return [
              [32,25,45],   #110 at 44 degrees
              [33,0,20],
              [48,30,50],   #200 
              [49,05,25],
              [62,25,50],   #211
              [63, 0,25],
              [75,35,50],   #220
              [76,10,25],
              [106,10,36],  #222 
              [107,0,11] 
              ]
    elif crystal=="335" and takeoff==140 and nosteps==25:
        return [
               [32,0,18],
               [48,5,25],
               [62,0,20],
               [75,10,25]
               ]
    else:
       raise ValueError,"No V peak data found for %s at %s" % (crystal,takeoff)

def calc_eff_mark2(vanad,backgr,v_off,edge=((1,10),),norm_ref="bm3_counts",bottom = 22, top = 106, 
    detail=None,splice=None):
    """Calculate efficiencies given vanadium and background hdf files.  If detail is
    some integer, detailed calculations for that tube will be displayed. Edge is a
    list of tuples ((tube_no,step),) before which the tube is assumed to be blocked and therefore
    data are unreliable. All efficiencies in this area are set to 1.  A value for step larger
    than the total steps will result in zero efficiency for this tube overall. A splicing operation
    merges files in backgr by substituting the first splice steps of the first file with
    the first splice steps of the second file.

    The approach of this new version is to calculate relative efficiencies for each pixel at each step,
    then average them at the end.  This allows us to account for variations in illumination as
    a function of time, and to simply remove V coherent peaks rather than replace them with 
    neighbouring values.  It also gives us a decent estimate of the error.

    norm_ref is the source of normalisation counts for putting each frame and each dataset onto a
    common scale. Top and bottom are the upper and lower limits for a sensible signal."""

    import stat,datetime
    omega = vanad["mom"][0]  # for reference
    takeoff = vanad["mtth"][0]
    crystal = AddCifMetadata.pick_hkl(omega-takeoff/2.0,"335")  #post April 2009 used 335 only
    #
    # Get important information from the basic files
    #
    # Get file times from timestamps as older NeXuS files had bad values here
    #
    wl = AddCifMetadata.calc_wavelength(crystal,takeoff)
    vtime = os.stat(vanad.location)[stat.ST_CTIME]
    vtime = datetime.datetime.fromtimestamp(vtime)
    vtime = vtime.strftime("%Y-%m-%dT%H:%M:%S%z")
    btime = os.stat(backgr.location)[stat.ST_CTIME]
    btime = datetime.datetime.fromtimestamp(btime)
    btime = btime.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Subtract the background
    norm_target = applyNormalization(vanad,norm_ref,-1)
    applyNormalization(backgr,norm_ref,norm_target)
    pure_vanad = (vanad - backgr).get_reduced()    #remove the annoying 2nd dimension
    #
    # move the vertical pixels to correct positions
    #
    pure_vanad = getVerticallyCorrected(pure_vanad,v_off)
    nosteps = pure_vanad.shape[0]
    # now we have to get some efficiency numbers out.  We will have nosteps 
    # observations of each value, if nothing is blocked or scrubbed.   We obtain a
    # relative efficiency for every pixel at each height, and then average to
    # get a mean efficiency together with a standard deviation.
    #
    # We output a multiplier used for normalisation, so we need the inverse
    # of the observed relative value
    #
    # remember the structure of our data: the leftmost index is the vertical
    # pixel number, the right is the angle,
    eff_array = zeros(pure_vanad[0].shape)
    eff_error = zeros(pure_vanad[0].shape)
    # keep a track of excluded tubes by step to work around lack of count_zero
    # support
    tube_count = ones(pure_vanad.shape[0]) * pure_vanad.shape[-1]
    # Now zero out blocked areas. The first bs steps are blocked on tube bt.
    # We are assuming no overlap with V peaks later
    for bt,bs in edge:
        pure_vanad[0:bs,:,bt] = 0
        tube_count[0:bs] = tube_count[0:bs] - 1
    # Now zero out vanadium peaks
    sv_boundaries = scrub_vanad_pos(pure_vanad,takeoff,crystal,nosteps=nosteps)
    for bt,bstart,bfinish in sv_boundaries:
        pure_vanad[bstart:bfinish,:,bt] = 0
        tube_count[bstart:bfinish] = tube_count[bstart:bfinish] - 1
    # Now zero out excluded regions
    pure_vanad = pure_vanad[:,bottom:top,:]
    print "Tube count by step: " + `tube_count.tolist()`
     # For each detector position, calculate a factor relative to the mean observed intensity
    # at that step.
    step_sum = pure_vanad.sum(0) #total counts at each step - meaning is different to numpy
    average = step_sum/(tube_count * (top - bottom))  #average value for gain normalisation
    print "Average intensity seen at each step: " + `average.tolist()`
    # No broadcasting, have to be clever.  We have to keep our storage in
    # gumpy, not Jython, so we avoid creating large jython lists by not
    # using map.
    step_gain = ones(pure_vanad.shape)
    for new,old,av in zip(range(len(step_gain)),pure_vanad,average):
        step_gain[new] = old/av
    step_gain = step_gain.transpose()  # so now have [tubeno,vertical,step]
    # Now each point in step gain is the gain of this pixel at that step, using
    # the total counts at that step as normalisation
    # We add the individual observations to obtain the total gain...
    # Note that we have to reshape in order to make the arrays an array of vectors so that
    # mean and covariance will work correctly.  After the reshape + transpose below, we
    # have shape[1]*shape[2] vectors that are shape[0] (ie number of steps) long.
    gain_as_vectors = step_gain.reshape([step_gain.shape[0],step_gain.shape[1]*step_gain.shape[2]]) 
    gain_as_vectors = gain_as_vectors.transpose()
    # count the non-zero contributions
    nonzero_contribs = zeros(gain_as_vectors.shape,dtype=float)
    nonzero_contribs[gain_as_vectors>0] = 1.0
    nz_sum = nonzero_contribs.sum(axis=0)
    gain_sum = gain_as_vectors.sum(axis=0)
    total_gain = gain_sum/nz_sum
    final_gain = total_gain.reshape([step_gain.shape[1],step_gain.shape[2]])
    print 'We have total gain: ' + `final_gain`
    print 'Shape ' + `final_gain.shape`
    eff_array[:,bottom:top] = 1.0/final_gain
    # Calculate the covariance of the final sum as the covariance of the
    # series of observations, divided by the number of observations
    cov_array = zeros(gain_as_vectors.shape,dtype=float)
    # Following is necessary to match dimensions
    total_gain = total_gain.reshape([total_gain.shape[0],1])
    print 'Shapes: ' + `cov_array[:,0].shape` + `gain_as_vectors[:,0].shape` + `total_gain.shape`
    for step in xrange(gain_as_vectors.shape[1]):
        print 'Covariance step %d' % step
        cov_array[:,step] = (gain_as_vectors[:,step] - total_gain)**2
    # Now ignore the points that are not observed before summing
    cov_array[gain_as_vectors<=0] = 0
    cov_sum = cov_array.sum(axis=0)
    cov_result = cov_sum/(nz_sum - 1)
    covariances = cov_result.reshape([step_gain.shape[1],step_gain.shape[2]])
    print 'We have covariances too! ' + `covariances.shape`
    print 'Writing to eff_error, shape ' + `eff_error[:,bottom:top].shape`
    #   eff_error[tube_no] = (variance*(inverse_val**4))
    eff_error[:,bottom:top] = covariances*(eff_array[:,bottom:top]**4)
    # pixel OK map...anything with positive efficiency but variance is no 
    # greater than the efficiency (this latter is arbitrary)return eff_array
    ok_pixels = zeros(eff_array.shape,dtype=int)
    ok_pixels[eff_array>0]=1
    pix_ok_map = zeros(eff_error.shape,dtype=int)
    pix_ok_map[eff_error > eff_array]=1
    print "OK pixels %d" % ok_pixels.sum() 
    print "Variance not OK pixels %d" % pix_ok_map.sum()
    # Now fix our output arrays to avoid NaN
    #eff_array = where(isnan(eff_array),0,eff_array)
    #eff_error = where(isnan(eff_error),0,eff_error)
    if splice: 
        backgr_str = backgr[0]+" + " + backgr[1]
        add_str = "data from %s up to step %d replaced with data from %s" % (backgr[0],splice,backgr[1])
    else: 
        backgr_str = backgr
        add_str = ""
    # create blocked tube information table
    ttable = ""
    for btube,bstep in edge:
       ttable = ttable + "  %5d%5d\n" % (btube,bstep) 
    return {"_[local]_efficiency_data":eff_array.transpose(),
            "_[local]_efficiency_variance":eff_error.transpose(),
            "contributors":pix_ok_map,
            "_[local]_efficiency_raw_data":os.path.basename(vanad.location),
            "_[local]_efficiency_raw_timestamp":vtime,
            "_[local]_efficiency_background_data":os.path.basename(backgr.location),
            "_[local]_efficiency_background_timestamp":btime,
            "_[local]_efficiency_determination_material":"Vanadium",
            "_[local]_efficiency_determination_method":"From flood field produced by 9mm V rod",
            "_[local]_efficiency_pd_instr_2theta_monochr_pre":takeoff,
            "_[local]_efficiency_determination_wavelength":wl,
            "_[local]_efficiency_monochr_omega":omega,
            "_[local]_efficiency_diffrn_radiation_monochromator":crystal,
            "_pd_proc_info_data_reduction":
             "Flood field data lower than values in following table assumed obscured:\n  Tube   Step\n " + ttable + add_str
            }

def output_2d_efficiencies(result_dict,filename,comment='',transpose=False):
    #We have to make sure that we have our array orientation correct. The
    # transpose flag signals that the data and error arrays should be transposed before
    # output
    outfile = open(filename,"w")
    outfile.write("#"+comment+"\n")
    #first two values are dimensions in C/Java order
    outfile.write("data_efficiencies\n")
    efficiencies = result_dict["_[local]_efficiency_data"]
    variances = result_dict["_[local]_efficiency_variance"]
    if transpose==True:
        print 'Transposing efficiencies'
        efficiencies = efficiencies.transpose()
        variances = variances.transpose()
    del result_dict["_[local]_efficiency_data"]
    del result_dict["_[local]_efficiency_variance"]
    outfile.write("_[local]_efficiency_number_of_tubes %d\n" % len(efficiencies[0]))
    outfile.write("_[local]_efficiency_number_vertical %d\n" % len(efficiencies))
    for key,val in result_dict.items():
        if key[0]=='_':           # CIF items only
            if not '\n' in str(val):
                outfile.write("%s '%s'\n" % (key,val))
            else:
                outfile.write("%s \n;\n%s\n;\n" % (key,val))
    outfile.write("loop_\n _[local]_efficiency_data\n _[local]_efficiency_variance\n")
    # In Gumpy iteration is much faster as __getitem__ involves a lot of code each and
    # every time - hence we have rewritten this as an iterator
    col_count = 0
    col_iter = array.ArraySliceIter(efficiencies)
    var_col_iter = array.ArraySliceIter(variances)
    try:
      while True:
        col = col_iter.next()
        col_var = var_col_iter.next()
        pix_iter = col.item_iter()
        pix_var_iter = col_var.item_iter()
        point_count = 0
        try:
            while True:
                point_count = point_count + 1
                if not point_count%5:               #multiple of 5
                    outfile.write("\n")
                #Use lots of significant figures for variances as will take sqrt later
                outfile.write("%8.5f %10.7f " % (pix_iter.next(), pix_var_iter.next()))
        except StopIteration:
            pass
        outfile.write("##End row %d\n" % (col_count))  #a line at the end of each tube
        print 'Finished row %d' % col_count
        col_count = col_count + 1
    except StopIteration:
       pass
    outfile.close()
    # Return keys to dictionary
    result_dict["_[local]_efficiency_data"] = efficiencies
    result_dict["_[local]_efficiency_variance"] = variances

def getVerticalEdges(rawdata,simple=True,output_filename=None):
    """Get the vertical edges of the Echidna tubes based on a simple edge
    finding algorithm. We assume the edges are parallel. The shifts are
    adjusted so that 63.5 is the centre."""
    import os,math
    ref_tube = 0   #all widths relative to the first tube
    rw = rawdata.transpose()
    results = []
    for tube in range(len(rw)):
        print "%d:" % tube,
        results.append(get_edges(rw[tube]))
    ref_tube_wid = results[ref_tube][1] - results[ref_tube][0]
    # ref_tube_val = results[ref_tube][0]+(ref_tube_wid/2.0)
    if output_filename != None:
        of1 = open(output_filename,"w")
        of1.write('#Vertical offsets calculated from %s\n' % os.path.basename(rawdata.location))
        of1.write('#Calculated by Gumtree Edge algorithm\n')
    print "#Results:\n"
    print "#Offsets of centres relative to ideal 63.5\n"
    print "#Tube Offset Error Scale Error Low High Diff   Val(L) Val(H)  Ideal(L) Ideal(H)\n"
    for tube in range(len(results)):
        thisres = results[tube]
        thiswid = float(thisres[1] - thisres[0])
        widvar = 1        #assume +/- 0.5 on each
        thisoff = thisres[0]+(thiswid/2.0) - 63.5
        offvar = 1
        scaleerr = sqrt(widvar)/ref_tube_wid
        print "%3d: %4.1f %4.1f %5.3f %4.3f %3d %3d (%2d)" % (tube,thisoff,sqrt(offvar),
        thiswid/ref_tube_wid,scaleerr,thisres[0],thisres[1],thiswid)
        if simple and output_filename != None:
            of1.write("%3d  %3d\n" % (tube+1,-1*math.floor(thisoff)))
    if output_filename != None:
        of1.close()
    return {"result":results}

def find_edge(edge_points):
    """Find the half-way value between the values at the beginning and end
       of the supplied array. The largest value must be at the end"""
    target_val = edge_points[0]+(edge_points[-1] - edge_points[0])/2.0
    for i in range(len(edge_points)):
          if edge_points[i]>target_val and edge_points[i+1]>target_val: break
    return i

def get_edges(whole_strip,edge_search=30):
    """Return the bottom and top edges of the strip, assuming that the edge
       occurs within edge_search pixels"""
    # Gumtree - we can't reverse an array, so we have to be tricky and 
    # multiply the end one by -1
    return (find_edge(whole_strip[0:edge_search]),
            len(whole_strip) - (edge_search - find_edge(-1.0*whole_strip[-edge_search:])))

def getVerticalCenteredAverage(ds, output_filename=None):
    print 'make vertical correction list...'

    # check arguments
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')
    # vertical weighted mean values for each column
    vwm     = zeros(ds.shape[1])
    vwm_sum = 0.0

    for x in xrange(len(vwm)):
        sw = 0.0 # summed weights
        ws = 0.0 # weighted sum

        ds_iter = ds[:, x].item_iter()
        for y in xrange(ds.shape[0]):
            val = ds_iter.next()
            sw += val
            ws += val * y

        # calculate weighted mean value
        vwm_val = ws / sw

        vwm[x]   = vwm_val
        vwm_sum += vwm_val

    # average value of vwm
    vwm_avg = vwm_sum / len(vwm)

    f = None
    try:
        # check if file needs to be created
        if output_filename:
            f = open(output_filename, 'w')

        # result
        rs      = zeros(ds.shape[1], int)
        rs_axis = rs.axes[0]

        # maximal used offset
        max_offset = 0

        rs_iter = rs.item_iter()
        for x in xrange(len(vwm)):
            x_index  = x + 1 # from [0..127] to [1..128]
            offset   = int(round(vwm_avg - vwm[x]))

            if abs(offset) > max_offset:
                max_offset = abs(offset)

            # update result
            rs_iter.next()
            rs_iter.set_curr(offset)
            rs_axis[x] = x_index

            if f != None:
                f.write("%-7i %i\n" % (x_index, offset))

        # finalize result
        rs.title = 'Vertical Corrections [based on %s]' % ds.location

        print 'maximal absolute offset:', max_offset

        return rs

    finally:
        if f != None:
            f.close()
