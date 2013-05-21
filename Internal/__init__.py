HISTORY_KEY_WORDS = ['drive',
                     'run'
                     'runscan', 
                     'Scan start',
                     'ERROR', 
                     'Counting aborted',
                     'BATCHSTART',
                     'BATCHEND',
                     'Exported'
                     ]
# Check which mode we are in
from java.lang import System
if System.getProperty('gumtree.runtime.configEnv.mode') == 'analysis':
    print 'Loading analysis-only initialisation'
    import Analysis_init
else:
    import Initialise