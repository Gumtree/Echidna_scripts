'''
@author:        davidm
@organization:  ANSTO

@version:  1.7.0.1
@date:     05/07/2012
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
from gumpy.vis.gplot import plot

from math import *
import os.path as path

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

class Reduction:
    
    epsilon = 1e-5 # has to be grater than zero
    
    ''' internal helper '''
    @staticmethod
    def _min(l, r):
        if l <= r:
            return l
        else:
            return r
    @staticmethod
    def _max(l, r):
        if l >= r:
            return l
        else:
            return r
    @staticmethod
    def _getCenters(boundaries):
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
    
    ''' public '''
    @staticmethod
    def applyNormalization(ds, reference, target):
        print 'normalization of', ds.title
                
        # check if reference/target is a number
        numericReference = isinstance(reference, (int, long, float))
        numericTarget    = isinstance(target   , (int, long, float))
            
        # check arguments
        if not numericReference:
            if reference.ndim != 1:
                raise AttributeError('reference.ndim != 1')
            if reference.shape[0] != ds.shape[0]:
                raise AttributeError('reference.shape[0] != ds.shape[0]')
        
        if not numericTarget:
            if target.ndim != 1:
                raise AttributeError('target.ndim != 1')
            if target.shape[0] != ds.shape[0]:
                raise AttributeError('target.shape[0] != ds.shape[0]')
        
        def apply(ds, f):
            ds               *= f
            ds.bm1_counts    *= f
            ds.bm2_counts    *= f
            ds.bm3_counts    *= f
            ds.detector_time *= f
            ds.total_counts  *= f
        
        # normalization
        if numericTarget:
            if numericReference:
                apply(ds, float(target) / reference)
            else:
                for i in xrange(ds.shape[0]):
                    apply(ds[i], float(target) / reference[i])
        
        else:
            if numericReference:
                for i in xrange(ds.shape[0]):
                    apply(ds[i], float(target[i]) / reference)
            else:
                for i in xrange(ds.shape[0]):
                    apply(ds[i], float(target[i]) / reference[i])
            
        print 'normalized:', ds.title
        # finalize result
        ds.title += ' (Normalized)'
    @staticmethod
    def getSummed(ds, floatCopy=True, applyStth=True, show=True):
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
             
        if show:
            plot(rs)
            
        return rs
    @staticmethod
    def getStitched(ds, show=True):
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
            axisX = Reduction._getCenters(axisX)

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
            
        if show:
            plot(rs)

        return rs
    @staticmethod
    def getDeadPixelMap(ds, show=True):
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
                
                if ds_iter.next() <= Reduction.epsilon: # to compensate for floating-point error
                    dp += 1
                    rs_iter.set_curr(1)
                    
        except StopIteration:
            pass
        
        # finalize result
        rs.title = ds.title + ' (Dead Pixels)'

        print 'dead pixels:', dp
        
        if show:
            plot(rs)
            
        return rs
    @staticmethod
    def getOutlierMap(ds, stdRange=3, show=True):
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
                
                if ds_val > Reduction.epsilon: # ignore dead pixels
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
                
                if (ds_val > Reduction.epsilon) and ((ds_val < vL) or (ds_val > vH)) : # ignore dead pixels
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

        if show:
            plot(rs)
            
        return rs
    @staticmethod
    def getOkMap(ds, stdRange=3, lowerBoundary=None, upperBoundary=None, show=True):
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
                
                if ds_val > Reduction.epsilon: # ignore dead pixels
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
                
                if ds_val > Reduction.epsilon: # ignore dead pixels
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

        if show:
            plot(rs)
            
        return rs
    @staticmethod
    def getStdMap(ds, show=True):
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
                
                if ds_val > Reduction.epsilon: # ignore dead pixels
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
                
                if ds_val > Reduction.epsilon: # ignore dead pixels
                    st_iter.set_curr((ds_val - avg) / std)
 
        except StopIteration:
            pass
           
        # finalize result
        st.title = ds.title + ' (Std-Map)'
        
        print 'average counts per pixel:', avg
        print 'standard deviation:', std
        print 'dead pixels:', ds.shape[0] * ds.shape[1] - px

        if show:
            plot(st)
            
        return st
    @staticmethod
    def getEfficiencyCorrectionMap(van, bkg, okMap=None, show=True):
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
                         
                if (ok_iter.next() > Reduction.epsilon) and (rs_val > Reduction.epsilon): # to compensate for floating-point error
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
        
        if show:
            plot(rs)
            
        return rs
    @staticmethod # incomplete
    def getVerticalIntegrated(ds, okMap=None, normalization=-1, show=True):
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
                        if (ok_val > Reduction.epsilon) and (ds_val > Reduction.epsilon): # to compensate for floating-point error
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
            rs.set_axes([Reduction._getCenters(ds.axes[1])])
            rs.axes[0].title = ds.axes[1].title

        if show:
            plot(rs)

        return rs
    @staticmethod
    def getVerticalCorrectionList(ds, algorithm='Vertically Centered Average', show=True, output_filename=None):
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
        
            if show:
                plot(rs)
            
            return rs
        
        finally:
            if f != None:
                f.close()
    
    ''' corrections '''
    @staticmethod
    def getBackgroundCorrected(ds, bkg, show=True):
        print 'background correction of', ds.title
                
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
        
            if show:
                plot(rs)
            
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
                for frame in xrange(ds.shape[0]):
                    rs[frame, 0] -= bkg[frame, 0]
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
    @staticmethod
    def getEfficiencyCorrected(ds, eff, show=True):
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
        
            if show:
                plot(rs)
            
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
    @staticmethod
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
    @staticmethod
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
                axes.append(Reduction._getCenters(axisX)) # add centered x-axis
                
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



