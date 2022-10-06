import unittest


class TestSum(unittest.TestCase):
    def test_builtin_sum(self):
        self.assertEqual(sum([1,2,3]),5,"Should be 6")



if __name__ == "__main__":
    unittest.main()


