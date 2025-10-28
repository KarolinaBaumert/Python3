import unittest
from Zadanie1 import calculate_discount

class MyTestCase(unittest.TestCase):
    def test_calculate_discount(self):
        self.assertEqual(calculate_discount(100, 0.2), 80.0)
        self.assertEqual(calculate_discount(50, 0), 50.0)
        self.assertEqual(calculate_discount(200, 1), 0.0)
        with self.assertRaises(ValueError):
            calculate_discount(100, -0.1)
        with self.assertRaises(ValueError):
            calculate_discount(100, 1.5)


if __name__ == '__main__':
    unittest.main()
