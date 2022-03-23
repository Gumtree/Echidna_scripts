# These routines interpolate data onto a regular grid
from copy import copy
from gumpy.nexus import *

def interpolate(full_data,dropped,real_steps,start_ang,binsize,npoints,h_correction=None):
    """Interpolate the data in full_data collected at real_steps onto a 
    regular angular grid given by points starting from start_ang and stepping 
    by binsize for a total of `npoints` points. If h_correction is provided,
    each tube's nominal position is adjusted by this amount."""
    ideal_pts = create_regular_grid(start_ang,binsize,npoints) #numpy linspace also good
    print "Ideal pts: " + repr(ideal_pts)
    print "Actual pt: " + repr(real_steps)
    new_data = array.zeros(full_data.shape)
    for one_tube in range(0,full_data.shape[1]):
        #debug = one_tube == 54
        if h_correction == None: h_shift = 0
        else:
            h_shift = h_correction[one_tube]

        real_pts = Array(real_steps) + h_shift
        interp_pts = find_interp_pts(real_pts,ideal_pts,binsize,dropped,max_dist=binsize*1.1)
        if debug:
            print "Act pts " + repr(real_pts+one_tube*1.25)
            print "Ideal pts" + repr(Array(ideal_pts) + one_tube*1.25)
            print "Interp: " + repr(interp_pts)
            
        new_data[:,one_tube] = apply_interp(full_data.storage[:,one_tube],real_pts,ideal_pts,interp_pts,dropped,debug=debug)
    full_data.storage = new_data
    return full_data

def create_regular_grid(start,step,n):
    """Create a set of ideal points"""
    return [start + i*step for i in range(0,n)]

def find_interp_pts(real_pts,ideal_pts,ideal_sep,dropped,max_dist=0.1):

    # Choose the two closest valid points

    adjusts = []
    npoints = len(real_pts)
    for i in range(len(real_pts)):

        # if perfect match no interpolation

        if real_pts[i] == ideal_pts[i]:
            adjusts.append((0,0))
            continue
        
        test_pt = i

        # get first valid real point in lower direction
        
        while test_pt >= 0 and \
              (ideal_pts[i] < real_pts[test_pt] or test_pt in dropped):
            test_pt -= 1

        if test_pt == -1:   #went off the lower limit, search up
            test_pt = i
            while test_pt in dropped: test_pt += 1
            next_pt = test_pt + 1
            while next_pt in dropped and next_pt < npoints: next_pt += 1
            if abs(ideal_pts[i] - real_pts[test_pt]) < max_dist:
                adjusts.append((test_pt,next_pt))
            else:
                print "No interpolation for pt %d" % i
                adjusts.append((0,0))
            continue
        
        # get first valid point in upper direction, test_pt is the lowest we can go

        lower_pt = test_pt
        test_pt = lower_pt + 1
        
        while test_pt < npoints - 1 and (ideal_pts[i] > real_pts[test_pt] or test_pt in dropped):
            test_pt += 1

        if test_pt >= npoints - 1:  #went off top, search down
            test_pt = npoints - 1
            while test_pt in dropped or test_pt == lower_pt: test_pt -= 1

        adjusts.append((lower_pt,test_pt))

    return adjusts

def apply_interp(full_data,tube_steps,ideal_pts,interp_pts,dropped,debug=False):
    """Interpolate the data in full_data onto a regular grid. Full_data
    is an array [step,tube_no] and tube_steps is the position of each
    step as recorded by the encoder.
    The interpolated value for each point x is 
    I(a) + (I(b)-I(a))/(b-a) * (x-a)."""

    new_data = array.zeros(full_data.shape)
    for pt in range(len(interp_pts)):
        if interp_pts[pt] == (0,0) or pt in dropped:
            new_data[pt] = full_data[pt]
            continue
        l,u = interp_pts[pt]
        shift = (full_data[u] - full_data[l])/(tube_steps[u]-tube_steps[l]) * (ideal_pts[pt]-tube_steps[u])
        if debug:
            print "Shift for %d: from %f by %f to %f" % (pt,full_data[u],shift, full_data[u]+shift)

        new_data[pt] = full_data[u]+ shift

    return new_data

def test_interp():
    """Test interpolation routines"""
    test_data = array.zeros((5,3))
    tube_steps = Array([0.5,1.25,1.75,2.5,4.33])
    tube_corr = [0.1,0.05,0.25]

    test_data[:,0] = [10.0 + i*10 for i in tube_steps]
    test_data[:,1] = [10.0 + i*10 for i in (tube_steps + tube_corr[1])]
    test_data[:,2] = [10.0 + i*10 for i in (tube_steps + tube_corr[2])]

    print "Test data: " + repr(test_data)
    full_data = Dataset(test_data)
    print "Shape is " + repr(full_data.shape)
    res = interpolate(full_data,[],tube_steps,0.0,1.0,5)
    print "Results: " + repr(res.transpose().storage)

    # now with dropped point in middle

    full_data = Dataset(test_data)
    res = interpolate(full_data,[2],tube_steps,0.0,1.0,5)
    print "Dropping 2: " + repr(res.transpose().storage)

    # now with a tube position correction

    full_data = Dataset(test_data)
    res = interpolate(full_data,[],tube_steps,0.0,1.0,5,h_correction=tube_corr)
    print "With pos correction: " + repr(res.transpose().storage)

        
        

        
    
