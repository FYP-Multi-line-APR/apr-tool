import unittest
import collect_context 

class TestCollectContext(unittest.TestCase):
    def testDivideFrontLineRangeIntoParts(self):
        lower_bound = 5
        upper_bound = 23
        width = 10
        result = collect_context.divide_front_line_range_into_parts(lower_bound, upper_bound, width)
        self.assertEqual(result, [(5, 13), (14, 23)])
    
    def testDivideBackLineRangeIntoParts(self):
        lower_bound = 5
        upper_bound = 23
        width = 10
        result = collect_context.divide_back_line_range_into_parts(lower_bound, upper_bound, width)
        self.assertEqual(result, [(5, 14), (15, 23)])