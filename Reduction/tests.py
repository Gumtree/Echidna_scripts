# Test files for data reduction.
# We create a simple array.
import unittest
from gumpy.nexus import *
from Reduction import reduction

class NormalisationTestCase(unittest.TestCase):
    def setUp(self):
        import copy
        self.core_array1 = [[1.0,2.0,4.0],[16.0,9.0,1.0]]
        self.core_array2 = [[25,25,25],[25.0,25.0,25.0]]
        # norm vals represents counts in a monitor detector, so we
        # should multiply by the values below to get the actual detected
        # counts
        norm_vals = [10.0,20.0,5.0,15.0]
        # repeat this core array 4 times
        test_array = []
        for i in range(4):
            test_array = test_array + [copy.deepcopy(self.core_array2)]
        self.test_array = Dataset(test_array)
        # now unnormalise
        for i in range(4):
            self.test_array[i] *= norm_vals[i]/20.0
        self.test_array.bm1_counts = Array(norm_vals)
        self.test_array.var = Array(self.test_array)
        
    def testNorm(self):
        """Test that we recover the correct values"""
        ds,target = reduction.applyNormalization(self.test_array,reference='bm1_counts',target=-1)
        result = ds.storage
        for i in range(4):
            # Convoluted syntax below to get all to work with nested lists
            testing = map(all,(result[i] == self.core_array2).tolist())
            self.failUnless(all(testing))
        self.failUnless(target == max(self.test_array.bm1_counts))

    def testVar(self):
        """Test correct calculation of variances"""
        ds,target = reduction.applyNormalization(self.test_array,reference='bm1_counts',target=-1)
        result = ds.var
        # Check a few random points
        """If norm val 1 is 20 (the maximum), then the scale factor is 1.0 for frame 1
        with a variance of 1*20/400 = 0.05. If the observed intensity is 25, then the
        variance should be 0.05 * 25 * 25 + 25*1.0*1.0 = 31.25 + 25.0 = 56.25"""
        self.failUnless(ds.var[1][1][1] == 56.25)
        """If norm val 0 is 10, scale is 2 for frame 0 and variance 2 * 20/(10*10) = 0.4
        So for observed intensity 12.5, variance is 0.4 * 12.5 * 12.5 + 12.5*2*2 =
        62.5 + 50 = 112.5"""
        self.failUnless(ds.var[0][0][0] == 112.5)

    def testMetadata(self):
        """Test that metadata is correctly produced"""
        ds,target = reduction.applyNormalization(self.test_array,reference='bm1_counts',target=-1)
        pf = ds.harvest_metadata("CIF")
        print `pf`
        self.failUnless("Data normalised to %f" % float(target) in str(pf["_pd_proc_info_data_reduction"]))

if __name__=="__main__":
    unittest.main()
