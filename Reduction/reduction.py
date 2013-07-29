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
    # Store reference name for later
    refname = str(reference)
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
    rs = ds.__copy__()
    copy_metadata_deep(rs,ds)  #NeXuS metadata
    rs.copy_cif_metadata(ds)   #CIF metadata
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
        info_string = "Data normalised to %f on %s with error propagation assuming counting statistics" % (float(target),refname)
    else:
        # interesting note - if we get here, we are passed a single reference number
        # and a negative target, meaning that we use the reference as the target and
        # end up multiplying by 1.0, so no need to do anything at all.
        target = reference
        info_string = "No normalisation applied to data."
    rs.add_metadata('_pd_proc_info_data_reduction',info_string, append=True)
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
    rs.copy_cif_metadata(ds)
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

    
def read_efficiency_cif(filename):
    """Return a dataset,variance stored in a CIF file as efficiency values"""
    import CifFile,time
    print 'Reading in %s as CIF at %s' % (filename,time.asctime())
    eff_cif = CifFile.CifFile(str(filename))
    print 'Finished reading in %s as CIF at %s' % (filename,time.asctime())
    eff_cif = eff_cif['efficiencies']
    eff_data = map(float,eff_cif['_[local]_efficiency_data']) 
    eff_var = map(float,eff_cif['_[local]_efficiency_variance']) 
    final_data = Dataset(Data(eff_data).reshape([128,128]))
    final_data.var = (Array(eff_var).reshape([128,128]))
    print 'Finished reading at %s' % time.asctime()
    return final_data,eff_cif
    
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
    totals = ds.intg(axis=axis)
    contrib_map = zeros(ds.shape,dtype=int)
    contrib_map[ds>0.1] = 1
    contribs = contrib_map.intg(axis=axis)
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
    totals.copy_cif_metadata(ds)

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
            mean_angle +=new_angle
            bunch_points += 1
            try:
                new_angle = axis_iter.next()
            except:
                break
        else:                #this point to far beyond beginning
            # for debugging
            
            nt_iter.next()
            ntv_iter.next()
            nt_iter.set_curr(total_intensity/bunch_points)
            ntv_iter.set_curr(total_variance/(bunch_points*bunch_points))
            new_axis.append(mean_angle/bunch_points)
            in_points += bunch_points
            # debugging
            #if in_points < 30:
            #    print '%d: new_totals[0:50] = ' % in_points + `new_totals.storage[0:50]`
            #    print '%d: total_intensity/bunch_points = %f/%f = %f' % (in_points,total_intensity,
            #                                                         bunch_points,total_intensity/bunch_points) 
            #    print '%d: mean angle %f' % (in_points,mean_angle/bunch_points)
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
    print 'Finished debunching, nt[1000] = %f' % new_totals[1000]
    nt_iter.next()
    ntv_iter.next()
    nt_iter.set_curr(total_intensity/bunch_points)
    ntv_iter.set_curr(total_variance/(bunch_points*bunch_points))
    new_axis.append(mean_angle/bunch_points)
    # Trim output arrays
    newlen = len(new_axis)
    print 'Clustered axis has length %d, running from %f to %f' % (newlen,new_axis[0],new_axis[-1])
    print 'Cluster factor %d/%d =  %f' % (len(totals),newlen,1.0*len(totals)/newlen)
    print 'Totals[1000] = %f, new totals[1000] = %f' % (totals[1000],new_totals[1000])
    new_totals = new_totals[:newlen]
    new_totals.copy_cif_metadata(totals)
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

def getBackgroundCorrected(ds, bkg, norm_ref=None, norm_target=-1):
    """Subtract the background from the supplied dataset, after normalising the
    background to the specified counts on monitor given in reference. Note that
    for Echidna the dimensions must match as a single data frame cannot contain
    an entire background for multiple frames."""
    print 'background correction of', ds.title

    # normalise
    if norm_ref:
        bkg,target = applyNormalization(bkg,norm_ref,norm_target)

    rs = ds.__copy__()  # for metadata
    # result
    rs = ds - bkg
    rs.copy_cif_metadata(ds)
    
        # ensure that result doesn't contain negative pixels
    
    rs[rs < 0] = 0

        # finalize result
    rs.title = ds.title + ' (B)'
    info_string = 'Background subtracted using %s' % str(bkg.title)
    if norm_ref:
        info_string += 'after normalising to %f using monitor %s.' % (norm_target,norm_ref)
    else:
        info_string += 'with no normalisation of background.'
    rs.add_metadata("_pd_proc_info_data_reduction",info_string,tag="CIF",append=True)

    return rs

def getEfficiencyCorrected(ds, (eff,eff_metadata)):
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
        rs.copy_cif_metadata(ds)
        # now include all the efficiency file metadata
        for key in eff_metadata.keys():
            if key not in ("_[local]_efficiency_data","_[local]_efficiency_variance"):
                rs.add_metadata(key,eff_metadata[key])

        print 'efficiency corrected frames:', rs.shape[0]

    else:
        raise AttributeError('ds.ndim != 2 or 3')

    return rs

def getVerticallyCorrected(ds, offsets_filename):
    print 'vertical correction of', ds.title

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
        rs.copy_cif_metadata(ds)
        if ds.ndim == 2:
            y_len  = ds.shape[0]
            getter = getter2d
            setter = setter2d
        else:
            y_len  = ds.shape[1]
            getter = getter3d
            setter = setter3d

        # print 'ds.shape: ' + `ds.shape`
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
                            # print 'x_index, offset:' + `x_index` + ' ' + `offset`
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
        rs.title = ds.title + ' (V)'

        print 'vertically corrected:', ds.title
        info_string = "Pixels vertically translated according to contents of file %s" % offsets_filename
        rs.add_metadata("_pd_proc_info_data_reduction",info_string,"CIF",append=True)
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
        rs.copy_cif_metadata(ds)

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
        rs.title = ds.title + ' (H)'
        info_string = "Ideal detector tube positions were adjusted based on standard file."
        rs.add_metadata("_pd_proc_info_data_reduction",info_string,"CIF",append=True)
        print 'horizontally corrected:', ds.title

        return rs

    finally:
        if f != None:
            f.close()

# Calculate adjusted gain based on matching intensities between overlapping
# sections of data from different detectors
def do_overlap(ds,iterno,algo="FordRollett"):
    import time
    from Reduction import overlap
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
    gain,dd,interim_result,residual_map,chisquared,oldesds,first_ave = \
        iterate_data(e[3:],pixel_step=1,iter_no=iterno)
    print 'Have gains at %f' % time.clock()
    # calculate errors based on full dataset
    # First get a full model
    model,wd,mv = overlap.apply_gain(b.transpose()[3:],b.var.transpose()[3:],pixel_step,gain)
    esds = overlap.calc_error_new(b.transpose()[3:],model,gain,pixel_step)
    print 'Have full model and errors at %f' % time.clock()
    """ The following lines are intended to improve efficiency
    by a factor of about 10, by using Arrays instead of datasets
    and avoiding the [] operator, which currently involves too
    many lines of Python code per invocation. Note that 
    ArraySectionIter.next() is also code heavy, so calculate the
    sections ourselves."""
    final_gains = array.ones(ds.shape[-1])
    final_gains[2:] = gain
    final_errors = array.zeros(ds.shape[-1])
    final_errors[2:] = esds
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
    cs.storage = rs
    cs.var = rs_var
    cs.copy_cif_metadata(ds)
    # prepare info for CIF file
    import math
    detno = map(lambda a:"%d" % a,range(len(final_gains)))
    gain_as_strings = map(lambda a:"%.4f" % a,final_gains)
    gain_esd = map(lambda a:"%.4f" % math.sqrt(a),final_errors)
    cs.harvest_metadata("CIF").AddCifItem((
        (("_[local]_detector_number","_[local]_refined_gain","_[local]_refined_gain_esd"),),
        ((detno,gain_as_strings,gain_esd),))
        )
    return cs,gain,esds,chisquared

# Do an iterative refinement of the gain values
def iterate_data(dataset,pixel_step=25,iter_no=5,pixel_mask=None,plot_clear=True,algo="FordRollett"):
    """Iteratively refine the gain. The pixel_step is the number of steps a tube takes before it
    overlaps with the next tube. iter_no is the number of iterations. Pixel_mask has a zero for any
    tube that should be excluded. Algo 'ford rollett' applies the algorithm of Ford and Rollet, 
    Acta Cryst. (1968) B24, p293"""
    import overlap
    start_gain = array.ones(len(dataset))
    if algo == "FordRollett":
        gain,first_ave,chisquared,residual_map,ar,esds = overlap.find_gain_fr(dataset,dataset,pixel_step,start_gain,pixel_mask=pixel_mask)
    else:
        gain,first_ave,chisquared,residual_map,esds = overlap.find_gain(dataset,dataset,pixel_step,start_gain,pixel_mask=pixel_mask)
    old_result = first_ave    #store for later
    chisq_history = [chisquared]
    for cycle_no in range(iter_no+1):
        esdflag = (cycle_no == iter_no)  # need esds as well
        if algo == "FordRollett":
            gain,interim_result,chisquared,residual_map,ar,esds = overlap.find_gain_fr(dataset,dataset,pixel_step,gain,arminus1=ar,pixel_mask=pixel_mask,errors=esdflag)
        else:
            gain,interim_result,chisquared,residual_map,ar,esds = overlap.find_gain(dataset,dataset,pixel_step,gain,pixel_mask=pixel_mask,errors=esdflag)
        chisq_history.append(chisquared)
        # Calculate the errors using the full, not truncated, dataset
    print 'Chisquared: ' + `chisq_history`
    return gain,dataset,interim_result,residual_map,chisquared,esds,first_ave
