# Input simple data formats

def load_params_from_pdcif(filename):
    """Load data reduction parameters from a pdCIF file previously output
       by these routines
    """
    from CifFile import CifFile
    cf = CifFile(filename)
    fb = cf[cf.keys()[0]]
    if fb.has_key("_[local]_proc_reduction_parameter"):
        result = zip(fb["_[local]_proc_reduction_parameter"],
                     fb["_[local]_proc_reduction_value"]
                     )
        return dict(result)
    return {}
