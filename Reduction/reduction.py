'''
@author:        davidm,jamesh
@organization:  ANSTO

@version:  1.7.0.1
@date:     14/02/2013
@source:   http://www.nbi.ansto.gov.au/echidna/scripts/reduction.py

'''

from ECH import *

from gumpy.nexus import *
from gumpy.commons.jutils import jintcopy

from math import *
import os.path as path
import AddCifMetadata

# Following is updated by git checkout
gitversion = "$Id$"

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

    #finalise result
    if applyStth:
        stth = rs.stth
        axis = rs.axes[1]
        for i in xrange(axis.size):
            axis[i] += stth

        axis.title = 'two theta'
        rs.stth    = 0

    print 'summed frames:', frame_count

    return rs

def getStitched(ds,ignore=None):
    """The returned dataset is 2D after each segment of data from the multiple detectors has
    been placed at the correct angular position.  Ignore is a string specifying which frames
    should be ignored.  The format is 'a:b,c:d' to ignore from a to b inclusive and from c to
    d inclusive."""
    print 'stitching of', ds.title

    # check arguments
    if ds.ndim != 3:
        raise AttributeError('ds.ndim != 3')
    if ds.axes[0].title != 'azimuthal_angle':
        raise AttributeError('ds.axes[0].title != azimuthal_angle')
    if ds.axes[2].title != 'x_pixel_angular_offset':
        raise AttributeError('ds.axes[2].title != x_pixel_angular_offset')

    if ignore is not None:
        drop_frames = parse_ignore_spec(ignore)
    else:
        drop_frames = set([])

    print 'Dropping frames ' + `drop_frames`
    frame_count = ds.shape[0]
    y_count     = ds.shape[1]
    x_count     = ds.shape[2]

    print 'Input shape:' + `ds.shape`
    print 'Input storage shape:' + `ds.storage.shape`
    print 'Input var shape:' + `ds.var.shape`
    print 'X axis length:' + `len(ds.axes[2])`
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
    # We have switched to an imgCIF description of the axes (see AddCifMetadata module). Therefore our
    # axis values are kept in a CIF loop
    stth_info = ds.harvest_metadata("CIF").GetLoop("_diffrn_scan_frame_axis.frame_id")
    for info_packet in stth_info:
        src_frame = int(getattr(info_packet,"_diffrn_scan_frame_axis.frame_id"))
        if src_frame not in drop_frames:
            stth = float(getattr(info_packet,"_diffrn_scan_frame_axis.angle"))
            container.extend(map(lambda (src_column, angle): (angle, src_frame, src_column), enumerate(axisX + stth)))

    # sort by angles
    container = sorted(container, key=lambda (angle, src_frame, src_column): angle)
    print 'Check: total angles %d' % len(container)

    # resulting dataset
    rs = zeros([y_count, x_count * (frame_count-len(drop_frames))])

    # copy meta data
    copy_metadata_deep(rs, ds[0]) # for Echidna second dimension is just legacy
    rs.copy_cif_metadata(ds)
    # for debugging, not otherwise used
    for src_frame in set(xrange(0, frame_count-1)) - drop_frames:
        ds_frame = ds[src_frame]

    # java helper
    ds_storage = ds.storage
    rs_storage = rs.storage

    ds_var = ds.var
    rs_var = rs.var

    src_org = [0, 0      , 0]    #origins and shapes for section copies
    src_shp = [1, y_count, 1]

    dst_org = [0      , 0]       #destinations
    dst_shp = [y_count, 1]

    # copy columns.  As container is already sorted, we are simply copying in
    # columns starting at the beginning and moving along the destination array
    for dst_column, (angle, src_frame, src_column) in enumerate(container):

        # update origins
        src_org[0] = src_frame
        src_org[2] = src_column  #i.e. tube number
        dst_org[1] = dst_column  #i.e. new tube position
        # copy storage
        rs_storage[:,dst_column] = ds_storage.get_section(src_org,src_shp)
        rs_var[:,dst_column] = ds_var.get_section(src_org,src_shp)

    # assign axis values
    rs.axes[0] = axisY
    rs.axes[1] = map(lambda (angle, src_frame, src_column): angle, container)

    # finalize result
    info_string = "\nData from individual detectors arranged in order of ascending angle."
    if len(drop_frames)>0:
        info_string += "\nFrames in the following list were excluded from the final dataset:\n"
        for i in sorted(drop_frames):
            info_string +="%d " % i
    rs.add_metadata("_pd_proc_info_data_reduction",info_string,tag="CIF",append=True)
    # axes
    rs.axes[0].title = ds.axes[1].title
    rs.axes[1].title = ds.axes[2].title
    print 'stitched:', ds.title
    rs.title = ds.title
    return rs

    
def parse_ignore_spec(ignore_string):
    """A helper function to parse a string of form a:b,c:d returning
    (a,b),(c,d)"""
    import re
    p = ignore_string.split(',')
    q = map(lambda a:a.split(':'),p)
    # q is now  a sequence of string values
    final = []
    for strval in q:
        try:
            ranges = map(lambda a:int(a.strip()),strval)
            if len(ranges) == 1:
                final.append(ranges[0])
            else:
                final = final + range(ranges[0],ranges[1]+1)
        except ValueError:
            pass
    return set(final)   # a set to avoid duplications

def read_efficiency_cif(filename):
    """Return a dataset,variance stored in a CIF file as efficiency values"""
    import time
    from Formats import CifFile
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
def getVerticalIntegrated(ds, okMap=None, normalization=-1, axis=1, cluster=0.0,top=None,bottom=None):
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
    if bottom is None or bottom < 0: bottom = 0
    if top is None or top >= ds.shape[0]: top = ds.shape[0]-1
    working_slice = ds[bottom:top,:]
    totals = working_slice.intg(axis=axis)
    contrib_map = zeros(working_slice.shape,dtype=int)
    contrib_map[working_slice>0.1] = 1
    contribs = contrib_map.intg(axis=axis)
    #
    # We have now reduced the scale of the problem by 100
    #
    # Normalise to the maximum number of contributors
    print 'Axes labels:' + `ds.axes[0].title` + ' ' + `ds.axes[1].title`
    max_contribs = float(contribs.max())
    #
    print 'Maximum no of contributors %f' % max_contribs
    contribs = contribs/max_contribs  #
    save_var = totals.var
    totals = totals / contribs        #Any way to avoid error propagation here?
    totals.var = save_var/contribs

    # finalize result
    totals.title = ds.title
    totals.copy_cif_metadata(ds)
    info_string = "Data were vertically integrated from pixels %d to %d (maximum number of contributors %d)." % (bottom,top,max_contribs)
    
    # normalize result if required
    if normalization > 0:
        totals *= (float(normalization) / totals.max())
        info_string += "The maximum intensity was then multiplied by %f." % (float(normalization)/ totals.max())
    # check if any axis needs to be converted from boundaries to centers
    new_axes = []
    for i in range(totals.ndim):
        if len(totals.axes[i]) == totals.shape[i] + 1:
            new_axes.append(getCenters(totals.axes[i]))
        else:
            new_axes.append(totals.axes[i])
        print 'Axis %d: %s' % (i,totals.axes[i].title)
    old_names = map(lambda a:a.name,totals.axes)
    old_units = map(lambda a:a.units,totals.axes)
    old_names[-1] = 'Two theta'
    old_units[-1] = 'Degrees'
    totals.set_axes(new_axes,anames=old_names,aunits=old_units)
    
    # Finally, cluster points together if they are close enough

    if cluster > 0:
        totals = debunch(totals,cluster)
        info_string += "Points within %f of one another were averaged (weighted)." % cluster
    totals.add_metadata("_pd_proc_info_data_reduction",info_string,append=True)
    axislist = map(lambda a:a.title,totals.axes)
    print 'Axes: ' + `axislist`
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
    nt_iter.next()
    ntv_iter.next()
    nt_iter.set_curr(total_intensity/bunch_points)
    ntv_iter.set_curr(total_variance/(bunch_points*bunch_points))
    new_axis.append(mean_angle/bunch_points)
    # Trim output arrays
    newlen = len(new_axis)
    print 'Clustered axis has length %d, running from %f to %f' % (newlen,new_axis[0],new_axis[-1])
    print 'Cluster factor %d/%d =  %f' % (len(totals),newlen,1.0*len(totals)/newlen)
    new_totals = new_totals[:newlen]
    new_totals.copy_cif_metadata(totals)
    new_totals.set_axes([new_axis],anames=[totals.axes[0].name],aunits = [totals.axes[0].units])
    new_totals.title = totals.title
    return new_totals

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
    rs.title = ds.title
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
        rs.title = ds.title
        print 'efficiency corrected frames:', 1

    elif ds.ndim == 3:
        # check arguments
        if ds.axes[0].title != 'azimuthal_angle':
            raise AttributeError('ds.axes[0].title != azimuthal_angle (%s)' % ds.axes[0].title)
        if ds.shape[1:] != eff.shape:
            raise AttributeError('ds.shape[1:] != eff.shape')

        # result
        rs = ds.__copy__()
        for frame in xrange(ds.shape[0]):
            rs[frame] *= eff

        # finalize result
        rs.title = ds.title
        rs.copy_cif_metadata(ds)
        # now include all the efficiency file metadata, except data reduction
        for key in eff_metadata.keys():
            if key not in ("_[local]_efficiency_data","_[local]_efficiency_variance","_pd_proc_info_data_reduction"):
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
        rs.title = ds.title

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
        rs.title = ds.title
        info_string = "Ideal detector tube positions were adjusted based on standard file."
        rs.add_metadata("_pd_proc_info_data_reduction",info_string,"CIF",append=True)
        print 'horizontally corrected:', ds.title

        return rs

    finally:
        if f != None:
            f.close()

def read_horizontal_corrections(filename):
    """Read a file containing a simple list of offset values, 1 per line"""
    axisX = []
    f = open(filename,'r')
    for line in f:
            if type(line) is str:
                line = line.strip()
                if (len(line) > 0) and not line.startswith('#'):
                    axisX.append(float(line))
    return axisX

def calculate_average_angles(tube_steps,angular_file,pixel_step,tube_sep):
    """Calculate the average angle of measurement for overlapping tubes, given the
    correction values for individual tubes in the file."""
    no_of_overlaps = int(round(len(tube_steps)/pixel_step))-1
    correction_array = Array(read_horizontal_corrections(angular_file))
    no_of_tubes = len(correction_array)
    counter = array.zeros(no_of_tubes+no_of_overlaps,int)
    final_values = array.zeros(no_of_tubes+no_of_overlaps,float)
    for stepno in range(no_of_overlaps+1):
        counter[stepno:stepno+no_of_tubes]+=array.ones(no_of_tubes,int)
        final_values[stepno:stepno+no_of_tubes]+=correction_array
    ave_angles = final_values/counter
    print 'Check: average angles ' + `ave_angles`
    print 'Check: counter' + `counter`
    print 'Check: no of overlaps, tubes: %d %d ' % (no_of_overlaps,no_of_tubes)
    # Now apply these average corrections to the actual angles
    final_values = array.zeros((no_of_tubes+no_of_overlaps)*pixel_step)
    print 'Final values has len %d' % len(final_values)
    for stepno in range(no_of_tubes+no_of_overlaps):
        final_values[stepno*pixel_step:(stepno+1)*pixel_step] = tube_steps + tube_sep*stepno + ave_angles[stepno]
    return final_values

# Calculate adjusted gain based on matching intensities between overlapping
# sections of data from different detectors
def do_overlap(ds,iterno,algo="FordRollett",ignore=3,unit_weights=True,top=None,bottom=None,
               exact_angles=None):
    """Calculate rescaling factors for tubes based on overlapping data
    regions. The ignore parameter specifies the number of initial tubes for
    which data are unreliable and should be ignored. Specifying unit weights
    = False will use the variances contained in the input dataset. Note that
    the output dataset has already been vertically integrated as part of the
    algorithm. The vertical integration limits are set by top and bottom, if
    None all points are included. Exact_angles either contains the name of a
    file with per-detector angular corrections, or None."""
    import time
    from Reduction import overlap
    # Get sensible values
    if top is None: top = ds.shape[1]-1
    if bottom is None: bottom = 0
    b = ds[:,bottom:top,:].intg(axis=1).get_reduced()
    # Determine pixels per tube interval
    tube_pos = ds.axes[-1]
    tubesep = abs(tube_pos[0]-tube_pos[-1])/(len(tube_pos)-1)
    tube_steps = ds.axes[0]
    bin_size = abs(tube_steps[0]-tube_steps[-1])/(len(tube_steps)-1)
    pixel_step = int(round(tubesep/bin_size))
    bin_size = tubesep/pixel_step
    print '%f tube separation, %d steps before overlap, ideal binsize %f' % (tubesep,pixel_step,bin_size)
    # Reshape with individual sections summed
    c = b.reshape([b.shape[0]/pixel_step,pixel_step,b.shape[-1]])
    print `b.shape` + "->" + `c.shape`
    if c.shape[0] == 1:   #can't be done, there is no overlap
        return None,None,None,None
    # sum the individual unoverlapped sections
    d = c.intg(axis=1) #array of [rangeno,stepno,tubeno]
    e = d.transpose()  #array of [rangestep,tubeno]
    gain,dd,interim_result,residual_map,chisquared,oldesds,first_ave,weights = \
        iterate_data(e[ignore:],pixel_step=1,iter_no=iterno,unit_weights=unit_weights)
    # calculate errors based on full dataset
    # First get a full model
    start_ds = b.transpose()[ignore:] #array of [tubeno,stepno]
    start_var = start_ds.var
    model,wd,model_var = overlap.apply_gain(start_ds,1.0/start_var,pixel_step,gain,calc_var=True)
    # model and model_var have shape tubeno*pixel_step + no_steps (see shift_tube_add_new)
    esds = overlap.calc_error_new(start_ds,model,gain,pixel_step)
    print 'Have full model and errors at %f' % time.clock()
    cs = Dataset(model)
    cs.var = model_var
    # Now build up the important information
    cs.title = ds.title
    cs.copy_cif_metadata(ds)
    # construct the axes
    if exact_angles is None:
        axis = arange(len(model))
        new_axis = axis*bin_size + ds.axes[0][0] + ignore*pixel_step*bin_size
        axis_string = """Following this gain refinement, two theta values were recalculated assuming a step size of %8.3f 
and a tube separation of %8.3f starting at %f.""" % (bin_size,tubesep,ds.axes[0][0]+ignore*pixel_step*bin_size)
    else:
        new_axis = calculate_average_angles(tube_steps,exact_angles,pixel_step,tubesep)
        # Remove ignored tubes
        new_axis = new_axis[ignore*pixel_step:]
        
        axis_string = """Following this gain refinement, two theta values were recalculated using a tube separation of 
                         %8.3f and the recorded positions of the lowest angle tube, and then adding an average of the 
                         angular corrections for the tubes contributing to each two theta position.""" % (tubesep)
    cs.set_axes([new_axis],anames=['Two theta'],aunits=['Degrees'])
    print 'New axis goes from %f to %f in %d steps' % (new_axis[0],new_axis[-1],len(new_axis))
    print 'Total %d points in output data' % len(cs)
    # prepare info for CIF file
    import math
    detno = map(lambda a:"%d" % a,range(len(gain)))
    gain_as_strings = map(lambda a:"%.4f" % a,gain)
    gain_esd = map(lambda a:"%.4f" % math.sqrt(a),esds)
    cs.harvest_metadata("CIF").AddCifItem((
        (("_[local]_detector_number","_[local]_refined_gain","_[local]_refined_gain_esd"),),
        ((detno,gain_as_strings,gain_esd),))
        )
    info_string = "After vertical integration between pixels %d and %d," % (bottom,top) + \
        " individual tube gains were iteratively refined using the Ford/Rollett algorithm. Final gains " + \
        "are stored in the _[local]_refined_gain loop." + axis_string
    cs.add_metadata("_pd_proc_info_data_reduction",info_string,append=True)
    return cs,gain,esds,chisquared

# Do an iterative refinement of the gain values. We calculate errors only when chisquared shift is
# small, and aim for a shift/esd of <0.1
def iterate_data(dataset,pixel_step=25,iter_no=5,pixel_mask=None,plot_clear=True,algo="FordRollett",unit_weights=True):
    """Iteratively refine the gain. The pixel_step is the number of steps a tube takes before it
    overlaps with the next tube. Parameter 'dataset' is an n x m array, for m distinct angular regions covered by 
    detector number n. iter_no is the number of iterations, if negative the routine will iterate
    until chisquared does not change by more than 0.01 or abs(iter_no) steps, whichever comes first. Pixel_mask 
    has a zero for any tube that should be excluded. Algo 'ford rollett' applies the algorithm of Ford and Rollet, 
    Acta Cryst. (1968) B24, p293"""
    import overlap
    start_gain = array.ones(len(dataset))
    if unit_weights is True:
        weights = array.ones_like(dataset)
    else:
        weights = 1.0/dataset.var
    if algo == "FordRollett":
        gain,first_ave,ar,esds,k = overlap.find_gain_fr(dataset,weights,pixel_step,start_gain,pixel_mask=pixel_mask)
    else:
        gain,first_ave,esds = overlap.find_gain(dataset,dataset.var,pixel_step,start_gain,pixel_mask=pixel_mask)
    chisquared,residual_map = overlap.get_statistics_fr(gain,first_ave,dataset,dataset.var,pixel_step,pixel_mask)
    old_result = first_ave    #store for later
    chisq_history = [chisquared]
    k_history = [k]
    if iter_no > 0: 
        no_iters = iter_no
    else:
        no_iters = abs(iter_no)
    for cycle_no in range(no_iters+1):
        esdflag = (cycle_no == no_iters)  # need esds as well, and flags the last cycle
        if cycle_no > 3 and iter_no < 0:
            esdflag = (esdflag or (abs(chisq_history[-2]-chisq_history[-1]))<0.005)
        if algo == "FordRollett":
            gain,interim_result,ar,esds,k = overlap.find_gain_fr(dataset,weights,pixel_step,gain,arminus1=ar,pixel_mask=pixel_mask,errors=esdflag)
        else:
            gain,interim_result,ar,esds = overlap.find_gain(dataset,dataset,pixel_step,gain,pixel_mask=pixel_mask,errors=esdflag)
        chisquared,residual_map = overlap.get_statistics_fr(gain,interim_result,dataset,dataset.var,pixel_step,pixel_mask)
        chisq_history.append(chisquared)
        k_history.append(k)
        if esdflag is True:
            break
    print 'Chisquared: ' + `chisq_history`
    print 'K: ' + `k_history`
    print 'Total cycles: %d' % cycle_no
    print 'Maximum shift/error: %f' % max(ar/esds)
    return gain,dataset,interim_result,residual_map,chisq_history,esds,first_ave,weights

def get_stepsize(ds):
    """A utility function to determine the step size of the given dataset. This
    will only work if the data have not yet been stitched."""
    tube_pos = ds.axes[-1]
    tubesep = abs(tube_pos[0]-tube_pos[-1])/(len(tube_pos)-1)
    tube_steps = ds.axes[0]
    bin_size = abs(tube_steps[0]-tube_steps[-1])/(len(tube_steps)-1)
    pixel_step = int(round(tubesep/bin_size))
    bin_size = tubesep/pixel_step
    return bin_size

def merge_datasets(dslist):
    """Merge all of the datasets in dslist into a single dataset"""
    # We use a variant of our fast stitching routine
    # So first create a sorted list of angles and source files
    container = []
    print 'Passed %d datasets for merging ' % len(dslist)
    proc_info = """This dataset was created by collating points from multiple datasets. Data reduction 
    information for the individual source datasets is as follows:"""
    title_info = "Merge:"
    for num,dataset in enumerate(dslist):
        storage_info = zip(dataset.axes[0],dataset.storage,dataset.var.storage)
        container.extend(storage_info)
        proc_info += "\n\n===Dataset %s===\n" % str(dataset.title)
        try:
            proc_info += dataset.harvest_metadata("CIF")["_pd_proc_info_data_reduction"]
        except KeyError:
            pass
        title_info = title_info + dataset.title + ':'
    # So we have a list of angle,intensity,variance triples which we sort on angle
    container = sorted(container, key=lambda(angle,intensity,variance):angle)
    angles = map(lambda (a,b,c):a,container)
    intensities = map(lambda (a,b,c):b,container)
    variances = map(lambda (a,b,c):c,container)
    rs = Dataset(intensities)
    rs.var = variances
    rs.axes[0] = angles
    rs.axes[0].title = 'Two theta (degrees)'
    rs.title = title_info
    # Add metadata
    AddCifMetadata.add_standard_metadata(rs)
    rs.add_metadata("_pd_proc_info_data_reduction",proc_info,"CIF")
    return rs

def sum_datasets(dslist):
    """Add the provided datasets together"""
    #Assume all same length, same axis values
    newds = zeros_like(dslist[0])
    AddCifMetadata.add_standard_metadata(newds)
    title_info = ""
    proc_info = """This dataset was created by summing points from multiple datasets. Points were 
    assumed to coincide exactly. Data reduction information for the individual source datasets is as follows:"""
    for one_ds in dslist:
        newds += one_ds
        title_info = title_info + one_ds.title + "+"
        proc_info += "\n\n===Dataset %s===\n" % str(one_ds.title) 
        try:
            proc_info += one_ds.harvest_metadata("CIF")["_pd_proc_info_data_reduction"]
        except KeyError,AttributeError:
            pass
    newds.title = title_info[:-1]  #chop off trailing '+'
    newds.axes[0] = dslist[0].axes[0]
    # Add some basic metadata based on metadata of first dataset
    newds.copy_cif_metadata(dslist[0])
    newds.add_metadata('_pd_proc_info_data_reduction',proc_info,"CIF")
    return newds

def convert_to_dspacing(ds):
    if ds.axes[0].name != 'Two theta':
        return
    try:
        wavelength = float(ds.harvest_metadata("CIF")["_diffrn_radiation_wavelength"])
        print 'Wavelength for %s is %f' % (ds.title,wavelength)
    except KeyError:
        print 'Unable to find a wavelength, no conversion attempted'
        return   #Unable to convert anything
    # Funny call of sin below to avoid problems with sin being shadowed by the
    # standard maths library
    new_axis = wavelength/(2.0*(ds.axes[0]*3.14159/360.0).__sin__())
    ds.set_axes([new_axis],anames=['d-spacing'],aunits=['Angstroms'])
    return 'Changed'

def convert_to_twotheta(ds):
    if ds.axes[0].name != 'd-spacing':
        return
    try:
        wavelength = float(ds.harvest_metadata("CIF")["_diffrn_radiation_wavelength"])
    except KeyError:
        print 'Unable to find a wavelength, no conversion attempted'
        return   #Unable to convert anything
    print 'Wavelength for %s is %f' % (ds.title,wavelength)
    new_axis = arcsin(wavelength/(2.0*ds.axes[0]))*360/3.14159
    ds.set_axes([new_axis],anames=['Two theta'],aunits=['Degrees'])
    return 'Changed'
