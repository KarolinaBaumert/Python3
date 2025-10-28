import unittest
from Zadanie1 import count_vowels

class MyTestCase(unittest.TestCase):
    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("aeiouy"), 6)
        self.assertEqual(count_vowels("bcdfghjklmnpqrstvwxz"), 0)
        self.assertEqual(count_vowels("AEIOUY"), 6)


if __name__ == '__main__':
    unittest.main()
