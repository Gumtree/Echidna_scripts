import math

def write_cif_data(ds,filename):
    """Write the dataset in CIF format"""
    from StarFile import LoopBlock
    from datetime import datetime
    block_name = sanitise(ds.title[0:17])
    if not filename[-3:]=='cif':
        filename = filename+'.cif'
    fh = open(filename,"w")
    header = \
"""#CIF\1.1
#####################################################
#                                                   #
#   CIF file using powder CIF dictionary)           #
#   For details, see http://it.iucr.org/g           #
#                                                   #
#####################################################
"""
    fh.write(header)
    # Create a block name from dataset name and current time
    current_time = datetime.now().isoformat()
    fh.write("data_%s%s\n" % (block_name,current_time))
    # Create a unique block id
    username = '?'
    try:
        username = sanitise(str(ds['user']))
    except:
        pass
    fh.write("_pd_block_id \t%s|%s|%s\n" % (block_name,current_time,username) )
    fh.write("_audit_creation_date \t%s\n"% current_time)
    fh.write("_audit_creation_method \t%s\n"% "'Automatically generated from raw NeXuS data file by Gumtree routines'")
    fh.write("loop_\n _audit_conform_dict_name\n  _audit_conform_dict_version\n _audit_conform_dict_location\n")
    fh.write(" cif_core.dic  2.3.1 ftp://ftp.iucr.org/pub/cifdics/cif_core_2.3.1.dic\n")
    fh.write(" cif_pd.dic    1.0.1 ftp://ftp.iucr.org/pub/cifdics/cif_pd_1.0.1.dic\n\n")
    more_metadata = ds.harvest_metadata("CIF")
    for key,value in more_metadata.items():
        print "DEBUG: writing %s -> %s" % (key,str(value))
        fh.write("%s \t" % key)
        fh.write("%s\n" % prepare_string(str(value)))
    # now put in the actual data
    fh.write("\nloop_\n _pd_proc_2theta_corrected\n _pd_proc_intensity_net\n _pd_proc_intensity_net_esd\n")
    for point in range(len(ds)):
        fh.write("%10.5f %15s %15.5f\n" % (ds.axes[0][point],format_esd(ds[point],ds.var[point]),math.sqrt(ds.var[point])))
    fh.close()

def sanitise(badstring):
    """Remove dodgy characters from username"""
    badstring = badstring.replace(' ','-')
    return badstring.replace('_','-')

# A fairly primitive formatter that will break on pathological strings,
# for example semicolons as the first character in a line in a multi-line string
#
def prepare_string(bad_string):
    """Format a string for a CIF file"""
    if "\r" in bad_string or "\n" in bad_string:
        #Wrap the text nicely
        good_string = "\n;\n"+good_string+"\n;\n";
    else: 
       	# Note that this is not perfect; we may have a string containing whitespace
       	# immediately following a single or double quote, in which case we must use
       	# the semicolon-delimited variation.  We don't check for this here, but a
       	# simple regular expression should catch it
        if " " in bad_string or "\t" in bad_string:
            if "\"" in bad_string:
                good_string = "'" + bad_string + "'";
            else: 
                good_string = "\"" + bad_string + "\"";
        else: good_string = bad_string;
    return good_string;

#
def format_esd(number,var):
    """Format the esd as intensity(nn), where nn follows the ISO rules"""
    err = math.sqrt(var)
    if err<0.000000001: return "%.5f(0)" % number
    err_as_int = err
    outsigfigs = -2
    while err_as_int < 9.5: 
        outsigfigs+=1
        err_as_int *=10
    if outsigfigs < 0:
        flt_format = "%.0f(%2d)"
    else:
        flt_format = "%%.%df(%%2d)" % outsigfigs
    return flt_format % (number, int(round(err)))

###################################################
def dump_tubes(ds,filename):
    """Dump information from each tube"""
    import math
    # We have 2D data, with the first axis being tube number and the second
    # axis the angular step of that tube
    outfile = open(filename,"w")
    for tubeno in range(ds.shape[1]):
        outfile.write("#Detector %d\n" % tubeno)
        angle_array = ds.axes[0]+ds.axes[1][tubeno]
        data_array = ds[:,tubeno].get_reduced()
        error = data_array.var
        for stepno in range(ds.shape[0]):
            outfile.write("%8.4f   %8.4f    %8.4f" % (angle_array[stepno],data_array[stepno],
                                                      math.sqrt(error[stepno])))
            outfile.write("\n")
    outfile.close()
