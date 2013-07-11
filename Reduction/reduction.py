'''
@author:        davidm,jamesh
@organization:  ANSTO

@version:  1.7.0.1
@date:     14/02/2013
@source:   http://www.nbi.ansto.gov.au/echidna/scripts/reduction.py

'''

'''
Issues:
    !!! float_copy doesn't deep-copy meta data

    !!! Normalization doesn't effect monitor_data, detector_data, ...
    !!! Stitching - do I need to sum monitor_data, detector_data, etc ?
    
            rs.total_counts  += ds_frame.total_counts
            rs.monitor_data  += ds_frame.monitor_data
            rs.detector_time += ds_frame.detector_time
            rs.detector_data += ds_frame.detector_data

    following is assumed at the moment:
    
        bm1_counts ~ bm2_counts ~ bm3_counts ~ detector_time

'''

from ECH import *

from gumpy.nexus import *
from gumpy.commons.jutils import jintcopy

from math import *
import os.path as path
import AddCifMetadata

def copy_metadata_deep(ds, dfrom):
    ds.__copy_metadata__(dfrom, deep=True)
def copy_metadata_shallow(ds, dfrom):
    ds.__copy_metadata__(dfrom, deep=False)

# to supplement math-library 
def sqr(value):
    return value * value

class DefaultOkIter:
    def next(self):
        return 1 # always OK-pixel

epsilon = 1e-5 # has to be grater than zero
def _min(l, r):
        if l <= r:
            return l
        else:
            return r
def _max(l, r):
        if l >= r:
            return l
        else:
            return r
def getCenters(boundaries):
        # check dimensions
        if boundaries.ndim != 1:
            raise AttributeError('boundaries.ndim != 1')
        if boundaries.size < 2:
            raise AttributeError('boundaries.size < 2')
            
        # result
        rs = zeros(boundaries.size - 1) # result is one item shorter
        
        rs[:] = boundaries[0:-1]
        rs   += boundaries[1:]
        rs   *= 0.5

        return rs
    

def applyNormalization(ds, reference, target=-1):
    """Normalise datasets ds by multiplying by target/reference.  Beam monitor counts, count time and total counts are
       all adjusted by this amount.  Reference is a string referring to a particular location in the dataset, and
       target is the target value to which they will be adjusted.  If target is not specified, the maximum value of
       the reference array is used and reported for further use. The variance of the values in the reference array
       is assumed to follow counting statistics."""
    print 'normalization of', ds.title
    # Normalization
    reference = getattr(ds,reference)

    # check if reference/target is a number
    # TODO: gumpy doesn't allow us to handle a scalar with variance
    # for multiplying arrays, so we can't propagate variance at present
    numericReference = isinstance(reference, (int, long, float))
    
    # check arguments
    if not numericReference:
        if reference.ndim != 1:
            raise AttributeError('reference.ndim != 1')
        if reference.shape[0] != ds.shape[0]:
            raise AttributeError('reference.shape[0] != ds.shape[0] (%d != %d)' % (reference.shape[0],ds.shape[0]))

    def do_norm(rs, f, varf):
        # We propagate errors in the data, but not in
        # the ancillary values
        print 'In do_norm, given %f(%f)' % (f,varf)
        print 'In do_norm, before: ' + `rs.storage`
        # Funny syntax below to make sure we write into the original area,
        # not assign a new value
        rs.var *= f * f
        rs.var += varf * rs * rs
        rs.storage       *= f
        try:             #These may be absent in some cases
            rs.bm1_counts    *= f
            rs.bm2_counts    *= f
            rs.bm3_counts    *= f
            rs.detector_time *= f
            rs.total_counts  *= f
        except AttributeError:
            pass
       
    # normalization
    copy_metadata_deep(rs,ds)
    if numericReference and target > 0:
        # We have a single number to refer to for normalisation, so
        # we are effectively scaling everything by a single number
        scale_factor = float(target)/reference
        variance = scale_factor * target/(reference*reference)
        do_norm(rs, scale_factor, variance)
        info_string = "Data multiplied by %f with variance %f" % (scale_factor,variance)
    elif not numericReference:
        # Each step has a different value, and we manually perform the
        # error propagation 
        reference = Data(reference)
        if target <= 0:
            target = reference.max()
        for i in xrange(rs.shape[0]):
            f = float(target)/reference[i]
            v = f*target/(reference[i]*reference[i])
            # Funny syntax below to make sure we write into the original area,
            # not assign a new value
            tar_shape = [1,rs.shape[1],rs.shape[2]]
            tar_origin = [i,0,0]
            rss = rs.storage.get_section(tar_origin,tar_shape).get_reduced()
            rsv = rs.var.get_section(tar_origin,tar_shape).get_reduced()
            rs.var[i] = rsv*f * f
            rs.var[i] += v * rss * rss
            rs.storage[i] = rs.storage[i]*f
        info_string = "Data normalised to %f with error propagation assuming counting statistics" % float(target)
    else:
        # interesting note - if we get here, we are passed a single reference number
        # and a negative target, meaning that we use the reference as the target and
        # end up multiplying by 1.0, so no need to do anything at all.
        target = reference
        info_string = "No normalisation applied to data."
    rs.add_metadata('_pd_proc_info_data_reduction',info_string, tag="CIF", append=True)
    print 'normalized:', ds.title
    # finalize result
    rs.title += '-(N)'
    return rs,target

def getSummed(ds, floatCopy=True, applyStth=True):
    print 'summation of', ds.title

    # check arguments
    if ds.ndim != 3:
        raise AttributeError('ds.ndim != 3')
    if ds.axes[0].title != 'azimuthal_angle':
        raise AttributeError('ds.axes[0].title != azimuthal_angle')
    if applyStth and (ds.axes[2].title != 'x_pixel_angular_offset'):
        raise AttributeError('ds.axes[2].title != x_pixel_angular_offset')

    # first dimension is summed (for Echidna second dimension is just legacy)
    if floatCopy:
        rs = ds[0].float_copy()
    else:
        rs = ds[0].__copy__()

    frame_count = ds.shape[0]
    for frame in xrange(1, frame_count):
        ds_frame = ds[frame, 0]

        rs               += ds_frame
        rs.bm1_counts    += ds_frame.bm1_counts
        rs.bm2_counts    += ds_frame.bm2_counts
        rs.bm3_counts    += ds_frame.bm3_counts
        rs.detector_time += ds_frame.detector_time
        rs.total_counts  += ds_frame.total_counts

    # finalize result
    rs.title = ds.title + ' (Summed)'

    if applyStth:
        stth = rs.stth
        axis = rs.axes[1]
        for i in xrange(axis.size):
            axis[i] += stth

        axis.title = 'two theta'
        rs.stth    = 0

    print 'summed frames:', frame_count

    return rs

def getStitched(ds):
    print 'stitching of', ds.title

    # check arguments
    if ds.ndim != 3:
        raise AttributeError('ds.ndim != 3')
    if ds.axes[0].title != 'azimuthal_angle':
        raise AttributeError('ds.axes[0].title != azimuthal_angle')
    if ds.axes[2].title != 'x_pixel_angular_offset':
        raise AttributeError('ds.axes[3].title != x_pixel_angular_offset')
    if len(ds.stth) != ds.shape[0]:
        raise AttributeError('len(ds.stth) != ds.shape[0]')

    frame_count = ds.shape[0]
    y_count     = ds.shape[1]
    x_count     = ds.shape[2]

    axisY = ds.axes[1]
    axisX = ds.axes[2]

    # check if x-axis needs to be converted from boundaries to centers
    if len(axisX) == x_count + 1:
        axisX = getCenters(axisX)

    # container to sort columns
    container = []

    # add (angle, src_frame, src_column) for every frame and column.  
    # JRH explanation: src_frame is just the step number (ie frame number).  src_column is the tube
    # number.  Angle is the actual angle for this step and tube.
    # this neato code creates a list of (angle, step number, tube number) tuples where angle is the
    # actual angle that each column has come from.  The 'enumerate (axisX + stth)' phrase creates a list
    # of angles for each tube at each step (step position given by stth).
    for src_frame, stth in enumerate(ds.stth):
        container.extend(map(lambda (src_column, angle): (angle, src_frame, src_column), enumerate(axisX + stth)))

    # sort by angles
    container = sorted(container, key=lambda (angle, src_frame, src_column): angle)

    # resulting dataset
    rs = zeros([y_count, x_count * frame_count])

    # copy meta data
    copy_metadata_deep(rs, ds[0]) # for Echidna second dimension is just legacy
    for src_frame in xrange(1, frame_count):
        ds_frame = ds[src_frame]

        # !!! what needs to be added?
        rs.total_counts  += ds_frame.total_counts

    # java helper
    ds_storage = ds.storage.__iArray__.getArrayUtils()
    rs_storage = rs.storage.__iArray__.getArrayUtils()

    ds_var = ds.var.__iArray__.getArrayUtils()
    rs_var = rs.var.__iArray__.getArrayUtils()

    src_org = jintcopy([0, 0      , 0])    #origins and shapes for section copies
    src_shp = jintcopy([1, y_count, 1])

    dst_org = jintcopy([0      , 0])       #destinations
    dst_shp = jintcopy([y_count, 1])

    # copy columns.  As container is already sorted, we are simply copying in
    # columns starting at the beginning and moving along the destination array
    for dst_column, (angle, src_frame, src_column) in enumerate(container):

        # update origins
        src_org[0] = src_frame
        src_org[2] = src_column  #i.e. tube number
        dst_org[1] = dst_column  #i.e. new tube position

        # copy storage
        src_array = ds_storage.section(src_org, src_shp).getArray()
        dst_array = rs_storage.section(dst_org, dst_shp).getArray()
        src_array.getArrayUtils().copyTo(dst_array)

        # copy variance
        src_array = ds_var.section(src_org, src_shp).getArray()
        dst_array = rs_var.section(dst_org, dst_shp).getArray()
        src_array.getArrayUtils().copyTo(dst_array)

    # assign axis values
    rs.axes[0] = axisY
    rs.axes[1] = map(lambda (angle, src_frame, src_column): angle, container)

    # finalize result
    rs.title = ds.title + ' (Stitched)'
    # axes
    rs.axes[0].title = ds.axes[1].title
    rs.axes[1].title = ds.axes[2].title
    # sth/stth is included in x-axis
    rs.sth  = 0
    rs.stth = 0

    print 'stitched:', ds.title

    return rs

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
    
def read_efficiency_cif(filename):
    """Return a dataset,variance stored in a CIF file as efficiency values"""
    import CifFile,time
    print 'Reading in %s as CIF at %s' % (filename,time.asctime())
    eff_cif = CifFile.CifFile(str(filename))
    eff_cif = eff_cif['efficiencies']
    eff_data = map(float,eff_cif['_[local]_efficiency_data']) 
    eff_var = map(float,eff_cif['_[local]_efficiency_variance']) 
    final_data = Dataset(Data(eff_data).reshape([128,128]))
    final_data.var = (Array(eff_var).reshape([128,128]))
    print 'Finished reading at %s' % time.asctime()
    return final_data
    
# The following routine can be called with unstitched data, in
# which case we will return the data with the 'axis' dimension
# summed. The default is for axis=1
def getVerticalIntegrated(ds, okMap=None, normalization=-1, axis=1, cluster=0.0):
    print 'vertical integration of', ds.title
    start_dim = ds.ndim

    if (okMap is not None) and (okMap.ndim != 2):
        raise AttributeError('okMap.ndim != 2')

    # check shape
    if (okMap is not None) and (ds.shape != okMap.shape):
        raise AttributeError('ds.shape != okMap.shape')    

    # JRH strategy: we need to sum vertically, accumulating individual pixel
    # errors as we go, and counting the contributions.
    #
    # The okmap should give us contributions by summing vertically
    # Note that we are assuming at least 0.1 count in every valid pixel
    
    import time
    print `time.clock()`
    totals = ds.intg(axis=axis)
    print `time.clock()`
    contrib_map = zeros(ds.shape,dtype=int)
    print `time.clock()`
    contrib_map[ds>0.1] = 1
    print `time.clock()`
    contribs = contrib_map.intg(axis=axis)
    print `time.clock()`
    #
    # We have now reduced the scale of the problem by 100
    #
    # Normalise to the maximum number of contributors
    print 'Axes labels:' + `ds.axes[0].title` + ' ' + `ds.axes[1].title`
    max_contribs = float(contribs.max())
    #
    print 'Maximum no of contributors %f' % max_contribs
    contribs = contribs/max_contribs
    totals = totals / contribs
    
    # Note that we haven't treated variance yet

    # finalize result
    totals.title = ds.title + ' (Vertically Integrated)'

    # normalize result if required
    if normalization > 0:
        totals *= (float(normalization) / totals.max())
        totals.title = totals.title + ' (x %5.0f)' % (float(normalization)/totals.max())

    # check if any axis needs to be converted from boundaries to centers
    new_axes = []
    for i in range(totals.ndim):
        if len(totals.axes[i]) == totals.shape[i] + 1:
            new_axes.append(getCenters(totals.axes[i]))
        else:
            new_axes.append(totals.axes[i])
        print 'Axis %d: %s' % (i,totals.axes[i].title)
    totals.set_axes(new_axes)
    
    # Finally, cluster points together if they are close enough

    if cluster > 0:
        totals = debunch(totals,cluster)
    return totals

def debunch(totals,cluster_size):
    new_totals = zeros_like(totals)
    new_totals = Dataset(new_totals)
    nt_iter = new_totals.item_iter()
    ntv_iter = new_totals.var.item_iter()
    tot_iter = totals.item_iter()
    totv_iter = totals.var.item_iter()
    axis_iter = totals.axes[0].item_iter()
    cluster_begin = axis_iter.next()
    new_angle = cluster_begin
    total_intensity = total_variance = 0.0
    mean_angle = 0.0
    bunch_points = 0
    in_points = 0
    new_axis = []
    while True:
        distance = new_angle - cluster_begin
        if distance < cluster_size:
            total_intensity += tot_iter.next()
            total_variance += totv_iter.next()
            mean_angle +=axis_iter.next()
            bunch_points += 1
            try:
                new_angle = axis_iter.next()
            except:
                break
        else:                #this point to far beyond beginning
            nt_iter.next()
            ntv_iter.next()
            nt_iter.set_curr(total_intensity/bunch_points)
            ntv_iter.set_curr(total_variance/(bunch_points*bunch_points))
            new_axis.append(mean_angle/bunch_points)
            in_points += bunch_points
            # re-initialise counters
            total_intensity = 0.0
            total_variance = 0.0
            mean_angle = 0.0
            bunch_points = 0
            #The while loop has not stepped the input iterators forward, so we now treat the same
            #point as we have just tested, but as last_point will now be the same, we will accumulate
            #it.
            cluster_begin = new_angle
    # Now we have finished, we just need to handle the last point
    nt_iter.next()
    nt_iter.set_curr(total_intensity)
    new_axis.append(mean_angle/bunch_points)
    # Trim output arrays
    newlen = len(new_axis)
    new_totals = new_totals[:newlen]
    new_totals.axes[0] = new_axis
    new_totals.axes[0].title = totals.axes[0].title
    new_totals.title = totals.title
    return new_totals

def oldgetVerticalIntegrated(ds, okMap=None, normalization=-1):
    print 'vertical integration of', ds.title

    # check dimensions
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')
    if (okMap is not None) and (okMap.ndim != 2):
        raise AttributeError('okMap.ndim != 2')

    # check shape
    if (okMap is not None) and (ds.shape != okMap.shape):
        raise AttributeError('ds.shape != okMap.shape')    

    # result
    rs = ds[0].float_copy()
    rs.fill(0)
    # used to count integrated pixels (dependent on okMap and ds[x,y] > 0)
    rc = simpledata.instance(rs.shape, 0, int)

    # source iterators 
    ds_val_iter = ds.item_iter()
    ds_var_iter = ds.var.item_iter()

    # special check for okMap
    if okMap is not None:
        ok_iter = okMap.item_iter()
    else:
        ok_iter = DefaultOkIter()

    try:
        while True:
            # update source iterators
            ds_val = ds_val_iter.next()
            ds_var = ds_var_iter.next()
            # OK map
            ok_val = ok_iter.next()

            # target iterators (start over for every row)
            rs_val_iter = rs.item_iter()
            rs_var_iter = rs.var.item_iter()
            # used to count integrated pixels (dependent on okMap and ds[x,y] > 0)
            rc_iter = rc.item_iter()

            rs_val = rs_val_iter.next()
            rs_var = rs_var_iter.next()
            rc_val = rc_iter.next()

            try:
                while True:                
                    if (ok_val > epsilon) and (ds_val > epsilon): # to compensate for floating-point error
                        # accumulate events
                        rs_val_iter.set_curr(rs_val + ds_val)
                        rs_var_iter.set_curr(rs_var + ds_var)
                        # increase counter
                        rc_iter.set_curr(rc_val + 1)

                    # update target iterators
                    rs_val = rs_val_iter.next() # at the end of each row, the inner loop will break here
                    rs_var = rs_var_iter.next()
                    rc_val = rc_iter.next()

                    # update source iterators
                    ds_val = ds_val_iter.next()
                    ds_var = ds_var_iter.next()
                    ok_val = ok_iter.next()

            # for rs_val_iter
            except StopIteration:
                pass

    # ds_val_iter 
    except StopIteration:
        pass

    # execute normalization in regards to contributers
    rs_val_iter = rs.item_iter()
    rs_var_iter = rs.var.item_iter()
    rc_iter     = rc.item_iter()
    rc_max      = float(rc.max())
    try:
        while True:
            rs_val = rs_val_iter.next()
            rs_var = rs_var_iter.next()
            rc_val = rc_iter.next()

            # avoid division by zero
            if rc_val > 0:
                f = rc_max / rc_val
                rs_val_iter.set_curr(rs_val * (f))
                rs_var_iter.set_curr(rs_var * (f * f)) # f^2 for Poisson statistics

    except StopIteration:
        pass

    # finalize result
    rs.title = ds.title + ' (Vertically Integrated)'

    # normalize result if required
    if normalization > 0:
        rs *= (float(normalization) / rs.max())
        rs.title = rs.title + ' (Normalized)'

    # check if x-axis needs to be converted from boundaries to centers
    if len(ds.axes[1]) == (ds.shape[1] + 1):
        rs.set_axes([getCenters(ds.axes[1])])
        rs.axes[0].title = ds.axes[1].title

    return rs

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

''' corrections '''

def getBackgroundCorrected(ds, bkg, norm_ref=None, norm_target=-1):
    """Subtract the background from the supplied dataset, after normalising the
    background to the specified counts on monitor given in reference"""
    print 'background correction of', ds.title

    # normalise
    if norm_ref:
            applyNormalization(bkg,norm_ref,norm_target)

    if ds.ndim == 2:
        # check shape
        if ds.shape != bkg.shape:
            raise AttributeError('ds.shape != bkg.shape')

        # result
        rs = ds - bkg

        # ensure that result doesn't contain negative pixels
        rs[rs < 0] = 0

        # finalize result
        rs.title = ds.title + ' (Background Corrected)'

        print 'background corrected frames:', 1

    elif ds.ndim == 3:
        # check arguments
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')

        if bkg.ndim == 3:
            if bkg.axes[0].title != 'azimuthal_angle':
                raise AttributeError('bkg.axes[0].title != azimuthal_angle')
            if ds.shape != bkg.shape:
                raise AttributeError('ds.shape != bkg.shape')
        else:
            if ds.shape[1:] != bkg.shape:
                raise AttributeError('ds.shape[1:] != bkg.shape')

        # result
        rs = ds.__copy__()
        if bkg.ndim == 3:
            # subtract each bkg-frame from each rs-frame
            # can't we do this straight out?
            # for frame in xrange(ds.shape[0]):
            #    rs[frame, 0] -= bkg[frame, 0]
            rs = ds - bkg     # test this
        else:
            for frame in xrange(ds.shape[0]):
                rs[frame, 0] -= bkg

        # ensure that result doesn't contain negative pixels
        rs[rs < 0] = 0

        # finalize result
        rs.title = ds.title + ' (Background Corrected)'

        print 'background corrected frames:', ds.shape[0]

    else:
        raise AttributeError('ds.ndim != 2 or 3')

    return rs

def getEfficiencyCorrected(ds, eff):
    print 'efficiency correction of', ds.title

    # check dimensions
    if eff.ndim != 2:
        raise AttributeError('eff.ndim != 2')

    if ds.ndim == 2:
        # check shape
        if ds.shape != eff.shape:
            raise AttributeError('ds.shape != eff.shape')

        # result
       
        rs = ds * eff

        # finalize result
        rs.title = ds.title + ' (Efficiency Corrected)'

        print 'efficiency corrected frames:', 1

    elif ds.ndim == 3:
        # check arguments
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.shape[1:] != eff.shape:
            raise AttributeError('ds.shape[1:] != eff.shape')

        # result
        rs = ds.__copy__()
        for frame in xrange(ds.shape[0]):
            rs[frame] *= eff

        # finalize result
        rs.title = ds.title + ' (Efficiency Corrected)'

        print 'efficiency corrected frames:', rs.shape[0]

    else:
        raise AttributeError('ds.ndim != 2 or 3')

    return rs

def getVerticallyCorrected(ds, offsets_filename):
    print 'vertical correction of', ds.title

    # check arguments
    if ds.ndim == 2:
        if ds.axes[0].title != 'y_pixel_offset':
            raise AttributeError('ds.axes[0].title != y_pixel_offset')
    elif ds.ndim == 3:
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.axes[1].title != 'y_pixel_offset':
            raise AttributeError('ds.axes[2].title != y_pixel_offset')
    else:
        raise AttributeError('ds.ndim != 2 or 3')

    if not offsets_filename:
        raise AttributeError('offsets_filename is empty')

    f = None
    try:
        f = open(offsets_filename, 'r')

        # get functions for source data
        def getter2d(ds, src_sl, x_index):
            return ds[      src_sl, x_index] # 2d
        def getter3d(ds, src_sl, x_index):
            return ds[:, src_sl, x_index] # 3d

        # set functions for result data
        def setter2d(rs, dst_sl, x_index, value):
            rs[      dst_sl, x_index] = value # 2d
        def setter3d(ds, dst_sl, x_index, value):
            rs[:, dst_sl, x_index] = value # 3d

        rs = ds.__copy__()
        if ds.ndim == 2:
            y_len  = ds.shape[0]
            getter = getter2d
            setter = setter2d
        else:
            y_len  = ds.shape[2]
            getter = getter3d
            setter = setter3d

        for line in f:
            if type(line) is str:
                line = line.strip()
                if (len(line) > 0) and not line.startswith('#'):
                    items = line.split()
                    if len(items) == 2:
                        x_index  =  int(items[0]) - 1 # from [1..128] to [0..127]
                        offset   = -int(items[1])

                        # check if column has to be moved
                        if offset != 0:

                            # transfer pixel along current column
                            dst_sl = slice(
                                _max(-offset        , 0    ), 
                                _min(-offset + y_len, y_len))

                            src_sl = slice(                             
                                _max(+offset        , 0    ), 
                                _min(+offset + y_len, y_len))

                            setter(rs, dst_sl, x_index, getter(ds, src_sl, x_index))

                            # set cells outside to zero
                            if offset > 0:
                                dst_sl = slice(dst_sl.stop, y_len       )
                            else:
                                dst_sl = slice(0          , dst_sl.start)

                            setter(rs, dst_sl, x_index, 0)

        # finalize result
        rs.title = ds.title + ' (Vertically Corrected)'

        print 'vertically corrected:', ds.title

        return rs

    finally:
        if f != None:
            f.close()

def getHorizontallyCorrected(ds, offsets_filename):
    print 'horizontal correction of', ds.title

    # check arguments
    if ds.ndim == 2:
        if ds.axes[1].title != 'x_pixel_angular_offset':
            raise AttributeError('ds.axes[1].title != x_pixel_angular_offset')
    elif ds.ndim == 3:
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.axes[2].title != 'x_pixel_angular_offset':
            raise AttributeError('ds.axes[3].title != x_pixel_angular_offset')
    else:
        raise AttributeError('ds.ndim != 2 or 3')

    if not offsets_filename:
        raise AttributeError('offsets_filename is empty')

    f = None
    try:
        f = open(offsets_filename, 'r')

        rs = ds.__copy__()

        # get x-axis (last axis)
        axisX = rs.axes[-1]

        # check if x-axis needs to be converted from boundaries to centers
        if len(axisX) == (rs.shape[-1] + 1):
            axes = rs.axes[0:-1]                      # preserve other axes
            axes.append(getCenters(axisX)) # add centered x-axis

            rs.set_axes(axes)

            axisX       = rs.axes[-1]
            axisX.title = ds.axes[-1].title # preserve title of x-axis

        # read file
        index = 0
        for line in f:
            if type(line) is str:
                line = line.strip()
                if (len(line) > 0) and not line.startswith('#'):
                    axisX[index] += float(line)
                    index        += 1

        # finalize result
        rs.title = ds.title + ' (Horizontally Corrected)'

        print 'horizontally corrected:', ds.title

        return rs

    finally:
        if f != None:
            f.close()

def do_overlap(ds,iterno):
    import time
    b = ds.intg(axis=1).get_reduced()  
    # Determine pixels per tube interval
    tube_pos = ds.axes[-1]
    tubesep = abs(tube_pos[0]-tube_pos[-1])/(len(tube_pos)-1)
    tube_steps = ds.axes[0]
    bin_size = abs(tube_steps[0]-tube_steps[-1])/(len(tube_steps)-1)
    pixel_step = int(round(tubesep/bin_size))
    print '%d steps before overlap' % pixel_step
    # Reshape with individual sections summed
    c = b.reshape([b.shape[0]/pixel_step,pixel_step,b.shape[-1]])
    print `b.shape` + "->" + `c.shape`
    # sum the individual unoverlapped sections
    d = c.intg(axis=1)
    e = d.transpose()
    # we skip the first two tubes' data as it is all zero
    q= iterate_data(e[3:],pixel_step=1,iter_no=iterno)
    # q[0] contains the final gain values, which we now apply
    print 'Have gains at %f' % time.clock()
    """ The following lines are intended to improve efficiency
    by a factor of about 10, by using Arrays instead of datasets
    and avoiding the [] operator, which currently involves too
    many lines of Python code per invocation. Note that 
    ArraySectionIter.next() is also code heavy, so calculate the
    sections ourselves."""
    final_gains = array.ones(ds.shape[-1])
    final_gains[2:] = q[0]
    final_errors = array.zeros(ds.shape[-1])
    final_errors[2:] = q[5]
    ds_as_array = ds.storage
    rs = array.zeros_like(ds)
    rs_var = array.zeros_like(ds)
    gain_iter = final_gains.__iter__()
    gain_var_iter = final_errors.__iter__()
    print 'RS shape: ' + `rs.shape`
    print 'Gain shape: ' + `final_gains.shape`
    target_shape = [rs.shape[0],rs.shape[1],1]
    for atubeno in range(len(final_gains)):
        rta = rs.get_section([0,0,atubeno],target_shape)
        dta = ds_as_array.get_section([0,0,atubeno],target_shape)
        fgn = gain_iter.next()
        fgvn = gain_var_iter.next()
        rta += dta * fgn
        rtav = rs_var.get_section([0,0,atubeno],target_shape)
        # sigma^2(a*b) = a^2 sigma^2(b) + b^2 sigma^2(a)
        rtav += ds.var.storage.get_section([0,0,atubeno],target_shape)*fgn*fgn + \
                fgvn * dta**2
    # Now build up the important information
    cs = copy(ds)
    cs.data = rs
    cs.var = rs_var
    return cs,q

def iterate_data(dataset,pixel_step=25,iter_no=5,pixel_mask=None,plot_clear=True):
    import overlap
    start_gain = array.ones(len(dataset))
    gain,first_ave,chisquared,residual_map,esds = overlap.find_gain(dataset,dataset,pixel_step,start_gain,pixel_mask=pixel_mask)
    old_result = first_ave    #store for later
    chisq_history = [chisquared]
    for cycle_no in range(iter_no+1):
        esdflag = (cycle_no == iter_no)  # need esds as well
        gain,interim_result,chisquared,residual_map,esds = overlap.find_gain(dataset,dataset,pixel_step,gain,pixel_mask=pixel_mask,errors=esdflag)
        chisq_history.append(chisquared)
    print 'Chisquared: ' + `chisq_history`
    return gain,dataset,interim_result,residual_map,chisquared,esds,first_ave
