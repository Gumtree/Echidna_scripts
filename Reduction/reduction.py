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
       the reference array is used and reported for further use.  Note that the dataset is modified in place."""
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
            raise AttributeError('reference.shape[0] != ds.shape[0]')

    def do_norm(ds, f):
        ds               *= f
        ds.bm1_counts    *= f
        ds.bm2_counts    *= f
        ds.bm3_counts    *= f
        ds.detector_time *= f
        ds.total_counts  *= f

    # normalization
    if numericReference and target > 0:
        do_norm(ds, float(target) / reference)
        info_string = "Data multiplied by %f" % float(target)/reference
    elif not numericReference:
        reference = Data(reference)
        print "Norm array is %s" % `reference`
        if target <= 0:
            target = reference.max()
        for i in xrange(ds.shape[0]):
            do_norm(ds[i], float(target) / reference[i])
        info_string = "Data normalised to %f, no error propagation" % float(target)
    else:
        # interesting note - if we get here, we are passed a single reference number
        # and a negative target, meaning that we use the reference as the target and
        # end up multiplying by 1.0, so no need to do anything at all.
        target = reference
        info_string = "No normalisation applied to data."
    ds.add_metadata('_pd_proc_info_data_reduction',info_string, tag="CIF", append=True)
    print 'normalized:', ds.title
    # finalize result
    ds.title += '-(N)'
    return target

def getSummed(ds, floatCopy=True, applyStth=True):
    print 'summation of', ds.title

    # check arguments
    if ds.ndim != 4:
        raise AttributeError('ds.ndim != 4')
    if ds.axes[0].title != 'azimuthal_angle':
        raise AttributeError('ds.axes[0].title != azimuthal_angle')
    if ds.axes[1].title != 'time_of_flight':
        raise AttributeError('ds.axes[1].title != time_of_flight')
    if applyStth and (ds.axes[3].title != 'x_pixel_angular_offset'):
        raise AttributeError('ds.axes[3].title != x_pixel_angular_offset')

    # first dimension is summed (for Echidna second dimension is just legacy)
    if floatCopy:
        rs = ds[0, 0].float_copy()
    else:
        rs = ds[0, 0].__copy__()

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
    if ds.ndim != 4:
        raise AttributeError('ds.ndim != 4')
    if ds.axes[0].title != 'azimuthal_angle':
        raise AttributeError('ds.axes[0].title != azimuthal_angle')
    if ds.axes[1].title != 'time_of_flight':
        raise AttributeError('ds.axes[1].title != time_of_flight')
    if ds.axes[3].title != 'x_pixel_angular_offset':
        raise AttributeError('ds.axes[3].title != x_pixel_angular_offset')
    if len(ds.stth) != ds.shape[0]:
        raise AttributeError('len(ds.stth) != ds.shape[0]')

    frame_count = ds.shape[0]
    y_count     = ds.shape[2]
    x_count     = ds.shape[3]

    axisY = ds.axes[2]
    axisX = ds.axes[3]

    # check if x-axis needs to be converted from boundaries to centers
    if len(axisX) == x_count + 1:
        axisX = getCenters(axisX)

    # container to sort columns
    container = []

    # add (angle, src_frame, src_column) for every frame and column
    for src_frame, stth in enumerate(ds.stth):
        container.extend(map(lambda (src_column, angle): (angle, src_frame, src_column), enumerate(axisX + stth)))

    # sort by angles
    container = sorted(container, key=lambda (angle, src_frame, src_column): angle)

    # resulting dataset
    rs = zeros([y_count, x_count * frame_count])

    # copy meta data
    copy_metadata_deep(rs, ds[0, 0]) # for Echidna second dimension is just legacy
    for src_frame in xrange(1, frame_count):
        ds_frame = ds[src_frame, 0]

        # !!! what needs to be added?
        rs.total_counts  += ds_frame.total_counts

    # java helper
    ds_storage = ds.storage.__iArray__.getArrayUtils()
    rs_storage = rs.storage.__iArray__.getArrayUtils()

    ds_var = ds.var.__iArray__.getArrayUtils()
    rs_var = rs.var.__iArray__.getArrayUtils()

    src_org = jintcopy([0, 0, 0      , 0])
    src_shp = jintcopy([1, 1, y_count, 1])

    dst_org = jintcopy([0      , 0])
    dst_shp = jintcopy([y_count, 1])

    # copy columns
    for dst_column, (angle, src_frame, src_column) in enumerate(container):

        # update origins
        src_org[0] = src_frame
        src_org[3] = src_column
        dst_org[1] = dst_column

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
    rs.axes[0].title = ds.axes[2].title
    rs.axes[1].title = ds.axes[3].title
    # sth/stth is included in x-axis
    rs.sth  = 0
    rs.stth = 0

    print 'stitched:', ds.title

    return rs

def getDeadPixelMap(ds):
    print 'searching for dead pixels of', ds.title

    # check arguments
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')

    # result
    rs = ds.__copy__()
    rs.fill(0)
    dp = 0 # dead pixels

    ds_iter = ds.item_iter()
    rs_iter = rs.item_iter()
    try:
        while True:
            rs_iter.next()

            if ds_iter.next() <= epsilon: # to compensate for floating-point error
                dp += 1
                rs_iter.set_curr(1)

    except StopIteration:
        pass

    # finalize result
    rs.title = ds.title + ' (Dead Pixels)'

    print 'dead pixels:', dp

    return rs

def getOutlierMap(ds, stdRange=3):
    print 'searching for outliers of', ds.title

    # check arguments
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')

    # determine average and standard deviation
    px = 0.0 # number of pixels used
    sm = 0.0 # sum of values required for mean value
    sq = 0.0 # sum of squared values required for standard deviation

    ds_iter = ds.item_iter()
    try:
        while True:
            ds_val = ds_iter.next()

            if ds_val > epsilon: # ignore dead pixels
                px += 1
                sm += ds_val
                sq += ds_val * ds_val

    except StopIteration:
        pass

    # average and standard deviation
    avg = sm / px
    std = sqrt(sq / px - avg * avg)

    # valid range
    vL = avg - stdRange * std
    vH = avg + stdRange * std

    # result
    rs = ds.__copy__()
    rs.fill(0)
    ot = 0 # number of outliers

    ds_iter = ds.item_iter()
    rs_iter = rs.item_iter()
    try:
        while True:
            rs_iter.next()
            ds_val = ds_iter.next()

            if (ds_val > epsilon) and ((ds_val < vL) or (ds_val > vH)) : # ignore dead pixels
                # new outlier
                ot += 1
                rs_iter.set_curr(1)

    except StopIteration:
        pass

    # finalize result
    rs.title = ds.title + ' (Outliers)'

    # dead pixels
    dpx = ds.shape[0] * ds.shape[1] - px

    print 'average counts per pixel:', avg
    print 'standard deviation:', std
    print 'outliers:', ot, '(sigma range:', str(stdRange) + ')'
    print 'dead pixels:', dpx
    print 'discarded pixels', dpx + ot

    return rs

def getOkMap(ds, stdRange=3, lowerBoundary=None, upperBoundary=None):
    """The Ok Map is ? """
    print 'generating OK-map of', ds.title

    # check arguments
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')

    # determine average and standard deviation
    px = 0.0 # number of pixels used
    sm = 0.0 # sum of values required for mean value
    sq = 0.0 # sum of squared values required for standard deviation

    # to check boundaries
    y      =  0
    x      = -1 # in order to start with (x=0,y=0) at first pixel
    stride = ds.shape[1]

    ds_iter = ds.item_iter()
    try:
        while True:
            ds_val = ds_iter.next()

            x += 1
            if x >= stride:
                y += 1
                x  = 0

            if (lowerBoundary is not None) and (y < lowerBoundary):
                continue
            if (upperBoundary is not None) and (y > upperBoundary) :
                continue

            if ds_val > epsilon: # ignore dead pixels
                px += 1
                sm += ds_val
                sq += ds_val * ds_val

    except StopIteration:
        pass

    # average / standard deviation
    avg = sm / px
    std = sqrt(sq / px - avg * avg)

    # valid range
    vL = avg - stdRange * std
    vH = avg + stdRange * std

    # result is OK-map
    rs = ds.__copy__()
    rs.fill(0)
    ot = 0 # number of outliers

    # to check boundaries
    y      =  0
    x      = -1 # in order to start with (x=0,y=0) at first pixel

    ds_iter = ds.item_iter()
    ok_iter = rs.item_iter()
    try:
        while True:
            ok_iter.next()
            ds_val = ds_iter.next()

            x += 1
            if x >= stride:
                y += 1
                x  = 0

            if (lowerBoundary is not None) and (y < lowerBoundary):
                continue
            if (upperBoundary is not None) and (y > upperBoundary) :
                continue

            if ds_val > epsilon: # ignore dead pixels
                if (vL <= ds_val) and (vH >= ds_val):
                    ok_iter.set_curr(1)   # in range
                else:
                    ot += 1               # new outlier

    except StopIteration:
        pass

    # finalize result
    rs.title = ds.title + ' (OK-Map)'

    # dead pixels
    dpx = ds.shape[0] * ds.shape[1] - px

    print 'average counts per pixel:', avg
    print 'standard deviation:', std
    print 'outliers:', ot, '(sigma range:', str(stdRange) + ')'
    print 'dead pixels:', dpx
    print 'discarded pixels', dpx + ot

    return rs

def getStdMap(ds):
    print 'generating Std-map of', ds.title

    # check arguments
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')

    # determine average and standard deviation
    px = 0.0 # number of pixels used
    sm = 0.0 # sum of values required for mean value
    sq = 0.0 # sum of squared values required for standard deviation

    ds_iter = ds.item_iter()
    try:
        while True:
            ds_val = ds_iter.next()

            if ds_val > epsilon: # ignore dead pixels
                px += 1
                sm += ds_val
                sq += ds_val * ds_val

    except StopIteration:
        pass

    # average
    avg = sm / px
    std = sqrt(sq / px - avg * avg)

    # result is standard deviation map
    st = ds.float_copy()
    st.fill(0)

    ds_iter = ds.item_iter()
    st_iter = st.item_iter()
    try:
        while True:
            st_iter.next()
            ds_val = ds_iter.next()

            if ds_val > epsilon: # ignore dead pixels
                st_iter.set_curr((ds_val - avg) / std)

    except StopIteration:
        pass

    # finalize result
    st.title = ds.title + ' (Std-Map)'

    print 'average counts per pixel:', avg
    print 'standard deviation:', std
    print 'dead pixels:', ds.shape[0] * ds.shape[1] - px

    return st

def scrub_vanad_pos(vanad,takeoff,crystal,nosteps=25):
    """Return a (tube,minstep,maxstep) list describing where
       vanadium peaks occur for these settings"""
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

def calc_eff_mark2(vanad,backgr,v_off,edge=((1,10),),norm_ref="bm3_counts",detail=None,splice=None):
    """Calculate efficiencies given vanadium and background hdf files.  If detail is
    some integer, detailed calculations for that tube will be displayed. Edge is a
    list of tuples ((tube_no,step),) before which the tube is assumed to be blocked and therefore
    data are unreliable. All efficiencies in this area are set to zero.  A value for step larger
    than the total steps will result in zero efficiency for this tube overall. A splicing operation
    merges files in backgr by substituting the first splice steps of the first file with
    the first splice steps of the second file.

    The approach of this new version is to calculate relative efficiencies for each pixel at each step,
    then average them at the end.  This allows us to account for variations in illumination as
    a function of time, and to simply remove V coherent peaks rather than replace them with 
    neighbouring values.  It also gives us a decent estimate of the error.

    norm_ref is the source of normalisation counts for putting each frame and each dataset onto a
    common scale."""

    import stat
    omega = vanad["$entry/instrument/crystal/omega"][0]  # for reference
    takeoff = vanad["$entry/instrument/crystal/takeoff"][0]
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
    norm_target = applyNormalization(vanad,reference,-1)
    applyNormalization(backgr,reference,norm_target)
    no_backgr = vanad - backgr
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
    # pixel number, the right is the angle, as we have transposed 
    #
    eff_array = zeros((128,128)) 
    # Now zero out blocked areas
    for bt,bs in edge:
        pure_vanad[0:bs,:,bt] = 0
    # Now zero out vanadium peaks
    sv_boundaries = scrub_vanad_pos(pure_vanad,takeoff,crystal,nosteps=nosteps)
    for bt,bstart,bfinish in sv_boundaries:
        pure_vanad[bstart:bfinish,:,bt] = 0
    # Now zero out excluded regions
    pure_vanad = pure_vanad[:,22:106:,:]
    # For each detector position, calculate a factor relative to the mean observed intensity
    # at that step.
    step_sum = pure_vanad.sum(1).sum(1) #total counts at this step
    non_zero = map(lambda a:numpy.nonzero(a),pure_vanad)
    non_zero = map(lambda a:len(a[0]),non_zero)    #count non-zero elements
    average = step_sum/non_zero  #average value for gain normalisation
    print "Average intensity seen at each step: " + `average`
    step_gain = pure_vanad.transpose()/average
    step_gain = step_gain.transpose()  
    # Now each point in step gain is the gain of this pixel at that step, using
    # the total counts at that step as normalisation
    # We add the individual observations to obtain the total gain...
    # Note that we have to reshape in order to make the arrays an array of vectors so that
    # mean and covariance will work correctly
    gain_as_vectors = step_gain.reshape(step_gain.shape[0],step_gain.shape[1]*step_gain.shape[2]) 
    nonzero_gain = map(lambda a:numpy.compress(a>0,a),gain_as_vectors.transpose())
    total_gain = map(lambda a:numpy.mean(numpy.array(a)),nonzero_gain)
    total_gain = numpy.array(total_gain).reshape(step_gain.shape[1],step_gain.shape[2])
    # Calculate the covariance of the final sum as the covariance of the
    # series of observations, divided by the number of observations
    covariances = map(numpy.cov,nonzero_gain)
    covariances = numpy.array(covariances)
    #count contributions
    num_obs = numpy.array(map(len,nonzero_gain),dtype='float32')
    #divide by contributions - 1
    covariances = covariances/(num_obs-1)
    covariances = covariances.transpose().reshape(step_gain.shape[1],step_gain.shape[2]) 
    # now insert into the return array as inverse values
    eff_array[:,22:106] = 1.0/(total_gain.transpose())
    #   eff_error[tube_no] = (variance*(inverse_val**4))
    eff_error[:,22:106] = covariances.transpose()*(eff_array[:,22:106]**4)
    # pixel OK map...anything with positive efficiency but variance is no 
    # greater than the efficiency (this latter is arbitrary)
    ok_pixels = numpy.where(eff_array>0)
    pix_ok_map = numpy.where(eff_error < eff_array,0,-1)
    print "OK pixels %d" % len(ok_pixels[0])  
    print "Variance not OK pixels %d" % sum(sum(pix_ok_map)) 
    # Now fix our output arrays to avoid NaN
    eff_array = numpy.where(numpy.isnan(eff_array),0,eff_array)
    eff_error = numpy.where(numpy.isnan(eff_error),0,eff_error)
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
    return {"_[local]_efficiency_data":eff_array,
            "_[local]_efficiency_variance":eff_error,
            "contributors":pix_ok_map,
            "_[local]_efficiency_raw_data":os.path.basename(vanad),
            "_[local]_efficiency_raw_timestamp":vtime,
            "_[local]_efficiency_background_data":os.path.basename(backgr),
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

def getEfficiencyCorrectionMap(van, bkg, okMap=None):
    print 'create efficiency correction map...'

    # [davidm] I do not recommend to automatically sum the input, because the result may not be normalized correctly
    # check if summation is required
    # (it does not matter if we subtract each bkg-frame from each van-frame and then sum the result or
    #  if we subtract the summed bkg-frames from the summed van-frames)
    #if van.ndim == 4:
    #    van = Reduction.getSummed(van, applyStth=False, show=False)
    #if bkg.ndim == 4:
    #    bkg = Reduction.getSummed(bkg, applyStth=False, show=False)

    # check dimensions
    if van.ndim != 2:
        raise AttributeError('van.ndim != 2')
    if bkg.ndim != 2:
        raise AttributeError('bkg.ndim != 2')
    if (okMap is not None) and (okMap.ndim != 2):
        raise AttributeError('okMap.ndim != 2')

    # check shape
    if van.shape != bkg.shape:
        raise AttributeError('van.shape != bkg.shape')
    if (okMap is not None) and (van.shape != okMap.shape):
        raise AttributeError('van.shape != okMap.shape')

    # result     
    rs  = van.float_copy()
    rs -= bkg

    # iterators
    rs_val_iter = rs.item_iter()
    rs_var_iter = rs.var.item_iter()
    # special check for okMap
    if okMap is not None:
        ok_iter = okMap.item_iter()
    else:
        ok_iter = DefaultOkIter()

    px = 0.0 # number of pixels used
    sm = 0.0 # sum of inverted values required for mean value

    try:
        while True:
            rs_val = rs_val_iter.next()
            rs_var_iter.next()

            if (ok_iter.next() > epsilon) and (rs_val > epsilon): # to compensate for floating-point error
                px += 1
                sm += rs_val
            else:
                # for bad-pixel set result to zero
                rs_val_iter.set_curr(0.0)
                rs_var_iter.set_curr(0.0)

    except StopIteration:
        pass

    # finalize result
    av = sm / px # average
    rs = av / rs # = 1 / (rs / av) # to obtain inverted result

    rs.title = 'Efficiency Map [based on %s]' % van.title

    return rs
 # incomplete

def getVerticalIntegrated(ds, okMap=None, normalization=-1):
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

def getVerticalCorrectionList(ds, algorithm='Vertically Centered Average', output_filename=None):
    print 'make vertical correction list...'

    # check arguments
    if ds.ndim != 2:
        raise AttributeError('ds.ndim != 2')
    if ds.axes[0].title != 'y_pixel_offset':
        raise AttributeError('ds.axes[0].title != y_pixel_offset')
    if ds.axes[1].title != 'x_pixel_angular_offset':
        raise AttributeError('ds.axes[1].title != x_pixel_angular_offset')
    if (algorithm is str) and (algorithm.lower() != 'vertically centered average'):
        raise AttributeError('currently only "Vertically Centered Average" is supported')

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
        rs.title = 'Vertical Corrections [based on %s via "%s"]' % (ds.title, algorithm)

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
            applyNormalisation(bkg,norm_ref,norm_target)

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

    elif ds.ndim == 4:
        # check arguments
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.axes[1].title != 'time_of_flight':
            raise AttributeError('ds.axes[1].title != time_of_flight')

        if bkg.ndim == 4:
            if bkg.axes[0].title != 'azimuthal_angle':
                raise AttributeError('bkg.axes[0].title != azimuthal_angle')
            if bkg.axes[1].title != 'time_of_flight':
                raise AttributeError('bkg.axes[1].title != time_of_flight')
            if ds.shape != bkg.shape:
                raise AttributeError('ds.shape != bkg.shape')
        else:
            if ds.shape[2:] != bkg.shape:
                raise AttributeError('ds.shape[2:] != bkg.shape')

        # result
        rs = ds.__copy__()
        if bkg.ndim == 4:
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
        raise AttributeError('ds.ndim != 2 or 4')

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

    elif ds.ndim == 4:
        # check arguments
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.axes[1].title != 'time_of_flight':
            raise AttributeError('ds.axes[1].title != time_of_flight')
        if ds.shape[2:] != eff.shape:
            raise AttributeError('ds.shape[2:] != eff.shape')

        # result
        rs = ds.__copy__()
        for frame in xrange(ds.shape[0]):
            rs[frame, 0] *= eff

        # finalize result
        rs.title = ds.title + ' (Efficiency Corrected)'

        print 'efficiency corrected frames:', rs.shape[0]

    else:
        raise AttributeError('ds.ndim != 2 or 4')

    return rs

def getVerticallyCorrected(ds, offsets_filename):
    print 'vertical correction of', ds.title

    # check arguments
    if ds.ndim == 2:
        if ds.axes[0].title != 'y_pixel_offset':
            raise AttributeError('ds.axes[0].title != y_pixel_offset')
    elif ds.ndim == 4:
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.axes[1].title != 'time_of_flight':
            raise AttributeError('ds.axes[1].title != time_of_flight')
        if ds.axes[2].title != 'y_pixel_offset':
            raise AttributeError('ds.axes[2].title != y_pixel_offset')
    else:
        raise AttributeError('ds.ndim != 2 or 4')

    if not offsets_filename:
        raise AttributeError('offsets_filename is empty')

    f = None
    try:
        f = open(offsets_filename, 'r')

        # get functions for source data
        def getter2d(ds, src_sl, x_index):
            return ds[      src_sl, x_index] # 2d
        def getter4d(ds, src_sl, x_index):
            return ds[:, 0, src_sl, x_index] # 4d

        # set functions for result data
        def setter2d(rs, dst_sl, x_index, value):
            rs[      dst_sl, x_index] = value # 2d
        def setter4d(ds, dst_sl, x_index, value):
            rs[:, 0, dst_sl, x_index] = value # 4d

        rs = ds.__copy__()
        if ds.ndim == 2:
            y_len  = ds.shape[0]
            getter = getter2d
            setter = setter2d
        else:
            y_len  = ds.shape[2]
            getter = getter4d
            setter = setter4d

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
                            dst_sl = slice(                             \
                                Reduction._max(-offset        , 0    ), \
                                Reduction._min(-offset + y_len, y_len))

                            src_sl = slice(                             \
                                Reduction._max(+offset        , 0    ), \
                                Reduction._min(+offset + y_len, y_len))

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
    elif ds.ndim == 4:
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle')
        if ds.axes[1].title != 'time_of_flight':
            raise AttributeError('ds.axes[1].title != time_of_flight')
        if ds.axes[3].title != 'x_pixel_angular_offset':
            raise AttributeError('ds.axes[3].title != x_pixel_angular_offset')
    else:
        raise AttributeError('ds.ndim != 2 or 4')

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



