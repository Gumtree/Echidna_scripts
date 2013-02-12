'''
@author:        nxi, davidm
@organization:  ANSTO

@version:  1.7.0.1
@date:     25/06/2012
@source:   http://www.nbi.ansto.gov.au/echidna/scripts/ECH/config.py

'''

from gumpy.nexus.dataset import DatasetFactory
from gumpy.nexus.dataset import Dataset

import os.path as path

ABSOLUTE_DATA_SOURCE_PATH = path.abspath(path.dirname(__file__) + '/../Data')
DICTIONARY_FILENAME       = 'path_table'

# set up WBT factory
DatasetFactory.__prefix__             = 'ECH'
DatasetFactory.__path__               = ABSOLUTE_DATA_SOURCE_PATH
# DatasetFactory.__normalising_factor__ = 'monitor_data' # or 'total_counts' or 'detector_time'

ECH = DatasetFactory()

# check if dictionary exists
dicpath = path.abspath(path.dirname(__file__) + '/' + DICTIONARY_FILENAME)
if path.exists(dicpath) :
    Dataset.__dicpath__ = dicpath
