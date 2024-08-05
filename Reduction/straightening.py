# Code based on original Java code, translated to Python by AI then
# rewritten.

import math
from gumpy.nexus import *
from ECH import *
from au.gov.ansto.bragg.echidna.dra.core import GeometryCorrection
import time

def correctGeometryjv(ds, radius, thetaVect, Zpvertic, bottom, top):

    # Use the built-in Java routine

    cg = GeometryCorrection()

    # Input items
    
    dsjv = ds.__iArray__
    zpjv = Zpvertic.__iArray__
    varjv = ds.var.__iArray__
    all_angles = ds.axes[1].__iArray__

    #Output items

    new_ds = dataset.instance([zpjv.size, thetaVect.size], dtype=float)
    contribs = array.instance([zpjv.size, thetaVect.size], dtype=int)
    
    new_ds.copy_cif_metadata(ds)
    
    contjv = contribs.__iArray__

    cg.correctGeometry(dsjv, all_angles, radius, thetaVect.__iArray__, zpjv, varjv, bottom, top, contjv,
                       new_ds.__iArray__, new_ds.var.__iArray__)
    print("Finished correcting geometry")

    # Assign axes

    new_ds.axes[0] = Zpvertic
    new_ds.axes[1] = thetaVect
    new_ds.title = ds.title + " (straightened)"
    return new_ds, contribs
    
def correctGeometrypy(ds, radius, thetaVect, Zpvertic, contribs):
    """
    Calculate correct two theta value for each input pixel in ds, excluding those
    values where contribs is zero. Contrib has same dimensions as ds. Only do
    first 50 angles to save time.
    """
    verPixels = len(Zpvertic)
    mScanxPixels = len(ds[0])
    thlen = len(thetaVect)
    mdtheta =  (thetaVect[-1] - thetaVect[0])/(thlen - 1)
    print "Theta grid spacing %f" % mdtheta
    print "Input grid %d x %d" % (verPixels, mScanxPixels)
    mdtheta = mdtheta * math.pi/180.0

    ncontr = zeros((verPixels, mScanxPixels))  # number of contributions
    if contribs is None:
        contribs = ones((verPixels, mScanxPixels))

    decurved_variance = zeros((verPixels, mScanxPixels))  # new variances
    decurved_data = zeros((verPixels, mScanxPixels))  # output data
    inTheta0 = thetaVect[0] * (math.pi)/180  # start angle, radians
    Jacobian = 0.0  # for storing the Jacobian
    maxJac = 0.0
    minJac = 5.0
    thetagrid = [t * math.pi/180.0 for t in thetaVect] # initialise theta grid
    radsq = radius**2  # precalculate for efficiency

    # Loop over every single pixel, assigning to appropriate bin
    
    #for i in range(mScanxPixels):   #Loop over horizontal coord
    start_time = time.clock()
    for i in range(10):
        inTheta = ds.axes[1][i] * (math.pi)/180  # convert to radians
        oldcos = math.cos(inTheta)

        print "%d..." % i,
        
        for j in range(verPixels):  #Loop over vertical position
            
            invz = Zpvertic[j]  # vertical offset for this vertical pixel coordinate
            xFactor = radius/math.sqrt(radsq + invz**2)
            cor2theta = math.acos(xFactor*oldcos)  # potential sign issues?
            #Jacobian = 1.0/math.sqrt(1.0 - math.cos(cor2theta)**2)*math.sin(inTheta)
            #if Jacobian > maxJac:
            #    maxJac = Jacobian
            #if Jacobian < minJac:
            #    minJac = Jacobian
            mNewPixels = int(round((cor2theta - inTheta0)/mdtheta)) #Pixel position
            if contribs[j][i] == 1:
                ncontr[j][mNewPixels] += 1
                decurved_data[j][mNewPixels] += ds[j][i]
                decurved_variance[j][mNewPixels] += ds.var[j][i]

    elapsed = time.clock()
    print "Finished full straightening transform in %f" % (elapsed - start_time) 
    contributor_mask = zeros((verPixels, mScanxPixels), dtype=int)
    nonzero = 0  # count nonzero pixels

    # Now remove any pixels that are on the edges, as determined by zero contributions
    
    #for i in range(mScanxPixels):
    for i in range(10):
        print "%d..." % i,
        maxvert = verPixels - 1
        for j in range(1, maxvert):
            nc_j_i = ncontr[j][i]
            nc_j_minus_1_i = ncontr[j-1][i]
            if nc_j_i > 0 and nc_j_minus_1_i > 0 and ncontr[j+1][i] > 0:
                contributor_mask[j][i] = 1
                nonzero += 1
                continue
            elif nc_j_i > 0 and nc_j_minus_1_i == 0:  # found a rising edge, discard this value
                decurved_data[j][i] = 0.0
                decurved_variance[j][i] = 0.0
                j += 1  # skip the new real edge value
                contributor_mask[j][i] = 1  # but it does contribute
                nonzero += 1
                continue
            elif nc_j_i == 0 and nc_j_minus_1_i > 0:  # a falling edge
                decurved_data[j-1][i] = 0.0
                decurved_variance[j-1][i] = 0.0
        if ncontr[0][i] > 0:
            contributor_mask[0][i] = 1
            nonzero += 1
        if ncontr[maxvert][i] > 0:
            contributor_mask[maxvert][i] = 1
            nonzero += 1

    elapsed = time.clock()
    print("Geometry transformation minimum, maximum Jacobian: %f %f" % (minJac, maxJac))
    print("Nonzero pixels in mask: %d" % nonzero)
    print("Elapsed time %f" % (elapsed - start_time))

    return decurved_data, decurved_variance, contributor_mask
