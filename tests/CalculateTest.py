import unittest
from Zadanie1 import calculate_discount

class MyTestCase(unittest.TestCase):
    def test_calculate_discount(self):
        self.assertEqual(calculate_discount(100, 0.2), 80)
        self.assertEqual(calculate_discount(50, 0.1), 45)
        self.assertRaises(ValueError, calculate_discount, 100, 1.5)
        self.assertRaises(ValueError, calculate_discount, 100, -0.5)


if __name__ == '__main__':
    unittest.main()
