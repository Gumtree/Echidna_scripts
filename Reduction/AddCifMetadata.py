# This CIF function takes a raw NeXuS file (preferably before any processing)
# and extracts the metadata that may otherwise be lost in subsequent steps. It
# is analogous to the AddMetadata routine in the old Java code.  We store the
# metadata in the file itself, but in a place that we know is preserved on copy.

from Formats.CifFile import CifBlock

fixed_table = {
"_pd_instr_geometry": 	"Cylindrical array of vertical detector tubes centred on " +
	    		"sample illuminated by monochromatic neutrons",
"_pd_instr_location": "Echidna High Resolution Powder Diffractometer at " +
	    		" OPAL facility, Bragg Institute, Australia",
"_pd_instr_soller_eq_spec/detc": "0.0833",
"_diffrn_measurement.device":"He3-tubes",
}

def add_metadata_methods(rawfile):
    # This is so crazy - we are going to hack into the class to create three new functions to
    # handle our metadata, completely bypassing the built-in methods. We do this because
    # we think leaving the metadata at the Python level is simpler, but subclassing the Dataset
    # class and initialising from a Dataset looks clunky and awkward.
    # Tag keyword is included for legacy reasons
    def p(self,key,value,tag="CIF",append=False):
        metadata_store = self.__dict__['ms']  #get around gumpy intercepting getattr
        if metadata_store.has_key(key) and append is True:
            metadata_store[key] = metadata_store[key] + '\n' + value
        else:
            metadata_store[key] = value

    def h(self,tag):
        return self.__dict__['ms']

    def c(self,old):
        self.__dict__['ms'] = old.__dict__['ms']

    rawfile.__dict__['ms'] = CifBlock()
    rawfile.__class__.__dict__['add_metadata'] = p
    rawfile.__class__.__dict__['harvest_metadata'] = h
    rawfile.__class__.__dict__['copy_cif_metadata'] = c

def add_standard_metadata(dataset):
    add_metadata_methods(dataset)
    for key,val in fixed_table.items():
        dataset.add_metadata(key,val,tag="CIF")
    dataset.add_metadata("_computing_data_reduction", "Gumtree Echidna/Python routines","CIF")
    dataset.add_metadata("_diffrn_radiation_probe", "neutron","CIF")

def extract_metadata(rawfile,codeversions={}):
    """This transfers NeXuS metadata to CIF metadata"""
    import datetime
    add_standard_metadata(rawfile)
    # get monochromator-related information
    mom = average_metadata(rawfile['$entry/instrument/crystal/omega'])
    tk_angle = average_metadata(rawfile['$entry/instrument/crystal/takeoff_angle'])
    # get the date
    date_form = datetime.datetime.strptime(str(rawfile['$entry/start_time']),"%Y-%m-%d %H:%M:%S")
    mono_change = datetime.datetime(2009,04,01)
    new_mono_change = datetime.datetime(2024,10,01)
    if date_form < mono_change or date_form > new_mono_change:
        monotype = "115"
    else:
        monotype = "335"
    hklval = pick_hkl(mom - tk_angle/2.0,monotype)
     
    if len(hklval)==3:      # i.e. h,k,l found
        rawfile.add_metadata("_pd_instr_monochr_pre_spec",
                  hklval + " reflection from Ge crystal, "+monotype+" cut",tag="CIF")
        wavelength = calc_wavelength(hklval,tk_angle)
        rawfile.add_metadata("_diffrn_radiation_wavelength","%.3f" % wavelength,tag="CIF")
        rawfile.add_metadata("_[local]_diffrn_radiation_wavelength_determination",
                  "Wavelength is calculated from monochromator hkl and takeoff angle and is therefore approximate",
                  tag="CIF")
        # The following is changed later if the primary collimator is found to be inserted
        rawfile.add_metadata("_pd_instr_divg_eq_src/mono","%.3f" % (0.099*2.0*wavelength),tag="CIF")
    # Do some logic to obtain collimator positions
    try:
        pcr = average_metadata(rawfile["$entry/instrument/collimator/primary_collimator_rotation"])
        pcx = average_metadata(rawfile["$entry/instrument/collimator/primary_collimator_translation"])
    except AttributeError:   # No pcr after October 2024
        coll_string = "No primary collimator"
    else:
       if pcx > 120 and pcr is not None: 
          if abs(pcr-360.0)<5 or abs(pcr) < 5:  # 5' collimator
             coll_string = "A 5' primary collimator pre-monochromator"
             rawfile.add_metadata("_pd_instr_divg_eq_src/mono","0.0833",tag="CIF")
          else:
             coll_string = "A 10' primary collimator pre-monochromator"
             rawfile.add_metadata("_pd_instr_divg_eq_src/mono","0.1667",tag="CIF")
       else: coll_string = "No primary collimator "

    try:
        scr = average_metadata(rawfile['$entry/sample/secondary_collimator'])
        if scr>0.5:
            coll_string += " and a 10' secondary collimator post-monochromator."
            rawfile.add_metadata("_pd_instr_divg_eq_mono/spec","0.1667",tag="CIF")
        else:
            coll_string += " and no secondary collimator."
        rawfile.add_metadata("_diffrn_radiation_collimation",coll_string,tag="CIF")
    except AttributeError:         #some early files are missing secondary collimator
        pass
#    # These values were in the CIF writing area of the Java routines, best put here
    try:
        program_release = str(rawfile["$entry/program_revision"])
    except AttributeError:
        program_release = str(rawfile["$entry/sics_release"])
    rawfile.add_metadata("_computing_data_collection",str(rawfile["$entry/program_name"]) + " " + \
                         program_release,"CIF")
    # List the code versions used for data reduction
    codelist = ""
    for key in codeversions.keys():
        codelist += "%-20s: %s\n" % (key,codeversions[key])
    rawfile.add_metadata("_computing_data_reduction", str("Gumtree Echidna/Python routines, Git versions:\n" + codelist),"CIF")
    rawfile.add_metadata("_pd_spec_special_details",sanitize(str(rawfile["$entry/sample/name"])),"CIF")
    rawfile.add_metadata("_[local]_data_collection_description",str(rawfile["$entry/sample/description"]),"CIF")
    start_time = str(rawfile["$entry/start_time"]).replace(" ","T")
    end_time = str(rawfile["$entry/end_time"]).replace(" ","T")
    rawfile.add_metadata("_pd_meas_datetime_initiated", start_time,"CIF")
    rawfile.add_metadata("_[local]_datetime_completed", end_time,"CIF")
    try:
        username = str(rawfile["user_name"])
    except:
        username = "?"
    rawfile.add_metadata("_pd_meas_info_author_name", sanitize(username),"CIF")
    rawfile.add_metadata("_pd_meas_info_author_email", str(rawfile[ "$entry/user/email"]),"CIF")
    rawfile.add_metadata("_pd_meas_info_author_phone", str(rawfile[ "$entry/user/phone"]),"CIF")
    rawfile.add_metadata("_pd_instr_2theta_monochr_pre","%.3f" % tk_angle,"CIF")
    rawfile.add_metadata("_pd_instr_dist_mono/spec", "%.1f" % average_metadata(rawfile[ "$entry/sample/mono_sample_mm"]),"CIF")
    rawfile.add_metadata("_pd_instr_dist_spec/detc","%.1f" % average_metadata(rawfile["$entry/instrument/detector/radius"]),"CIF")
    try:
        rawfile.add_metadata("_diffrn_source_power", "%.2f" % (average_metadata(rawfile["$entry/instrument/source/power"])*1000),"CIF")
    except AttributeError:  #sometimes source power is missing
        pass
    # imgCIF information about geometry
    # axis loop
    names = (('_axis.id','_axis.type','_axis.equipment','_axis.depends_on'),)
    values = [['source','gravity','stth','horizontal','vertical'],
              ['.','.','rotation','rotation','translation'],
              ['source','gravity','detector','detector','detector'],
              ['.','.','.','stth','stth']]
    rawfile.__dict__['ms'].AddCifItem((names,(values,)))
    radius = rawfile.__dict__['ms']["_pd_instr_dist_spec/detc"]
    # add the vectors:
    """
    source      0 0 1    . . .
    gravity     -1 0 0   . . .
    stth        1 0 0    . . .
    horizontal  1 0 0    . . .
    vertical    1 0 0    0 0 -728
    """
    vector_dict = {"_axis.vector[1]":['0','-1','1','1','1'],
                   "_axis.vector[2]":['0','0','0','0','0'],
                   "_axis.vector[3]":['1','0','0','0','0'],
                   "_axis.offset[1]":['.','.','.','.','.'],
                   "_axis.offset[2]":['.','.','.','.','.'],
                   "_axis.offset[3]":['1','0','0','0',"-"+radius]}
    rawfile.__dict__['ms'].AddToLoop('_axis.id',vector_dict)
    # Add information about the stth positions for later use
    rawfile.add_metadata("_diffrn_scan.id","1","CIF")
    rawfile.add_metadata("_diffrn_scan.frames",rawfile.shape[0],"CIF")
    frame_ids = map(lambda a:"%d" % a,range(rawfile.shape[0]))
    stths = rawfile.stth[:]
    names = (("_diffrn_scan_frame.frame_id","_diffrn_scan_frame.frame_number"),)
    values = [frame_ids,range(1,rawfile.shape[0]+1)]  #Spec says start from 1
    rawfile.__dict__['ms'].AddCifItem((names,(values,)))
    names = (("_diffrn_scan_frame_axis.frame_id","_diffrn_scan_frame_axis.axis_id",
              "_diffrn_scan_frame_axis.angle"),)
    values = [frame_ids,['stth']*rawfile.shape[0],map(float,stths)]
    rawfile.__dict__['ms'].AddCifItem((names,(values,)))
    return rawfile

def store_reduction_preferences(rawfile,prof_names,prof_values):
    """Store the preferences for all parameters used in data reduction"""
    names = (('_[local]_proc_reduction_parameter',
                                       '_[local]_proc_reduction_value'),)
    rawfile.__dict__['ms'].AddCifItem((names,((prof_names,prof_values),)))

def average_metadata(entrytable):
    try:
        return sum(entrytable)/len(entrytable)
    except:
        return entrytable    #assume is a non-collection object

def calc_wavelength(hklval, twotheta):
    import math
    h = int(hklval[0])
    k = int(hklval[1])
    l = int(hklval[2])
    d = 5.657906/math.sqrt(h*h + k*k + l*l)
    return 2*d*math.sin(math.pi*twotheta/360.0)

def pick_hkl(offset,monotype):
    """A simple routine to guess the monochromator hkl angle. The
    offset values can be found by taking the dot product of the monotype
    with the hkl values """
    if monotype == "115": 
        offset_table = {"337":15.43, "335":24.52, "331":60.94, "115":0.0}
    else:
        offset_table = {"004":40.31,"113":15.08,"115":24.52,"117":28.89,
                    "224":5.05,"228":20.84,"331":36.42,"333":14.42,
                    "337":9.096,"335":0.0}
    best = filter(lambda a:abs(abs(offset) - offset_table[a])<2.5,offset_table.keys())
    if len(best)>1 or len(best)==0: return "Unknown"
    return best[0]

def sanitize(instring):
    """Translate non-allowed characters in user-supplied strings"""
    return instring.encode('ascii','replace')
