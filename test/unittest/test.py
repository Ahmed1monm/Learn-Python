import unittest
from my_sum import sum

class TestSum(unittest.TestCase):
    def test_my_sum(self):
        '''
            Test if it can sum list of integers 
        '''
        ip = [1,2,3]
        result = sum(ip)
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()


    