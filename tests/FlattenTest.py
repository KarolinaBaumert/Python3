import unittest
from Zadanie1 import flatten_list

class MyTestCase(unittest.TestCase):
    def test_flatten_list(self):
        self.assertEqual(flatten_list([1, 2, 3]), [1, 2, 3])
        self.assertEqual(flatten_list([1, [2, 3], [4, [5]]]), [1, 2, 3, 4, 5])
        self.assertEqual(flatten_list([]), [])
        self.assertEqual(flatten_list([[[1]]]), [1])
        self.assertEqual(flatten_list([1, [2, [3, [4]]]]), [1, 2, 3, 4])



if __name__ == '__main__':
    unittest.main()
