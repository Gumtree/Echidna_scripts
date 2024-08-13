# Code based on original Java code, translated to Python by AI then
# rewritten.

import math
from gumpy.nexus import *
from ECH import *
from au.gov.ansto.bragg.echidna.dra.core import GeometryCorrection
def correctGeometryjv(ds, radius, thetaVect, Zpvertic, bottom, top, interp=False):

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

    if interp:
        cg.correctGeometryInterp(dsjv, all_angles, radius, thetaVect.__iArray__, zpjv, varjv, bottom, top, contjv,
                       new_ds.__iArray__, new_ds.var.__iArray__)
    else:        
        cg.correctGeometry(dsjv, all_angles, radius, thetaVect.__iArray__, zpjv, varjv, bottom, top, contjv,
                       new_ds.__iArray__, new_ds.var.__iArray__)
    print("Finished correcting geometry")

    # Assign axes

    new_ds.axes[0] = Zpvertic
    new_ds.axes[1] = thetaVect
    new_ds.title = ds.title + " (straightened)"
    return new_ds, contribs
