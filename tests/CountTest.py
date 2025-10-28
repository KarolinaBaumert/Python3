import unittest
from Zadanie1 import count_vowels

class MyTestCase(unittest.TestCase):
    def test_count_vowels(self):
        self.assertEqual(count_vowels("Python"), 1)
        self.assertEqual(count_vowels("AEIOUY"), 6)
        self.assertEqual(count_vowels("bcd"), 0)
        self.assertEqual(count_vowels(""), 0)
        self.assertEqual(count_vowels("Próba żółwia"), 4)


if __name__ == '__main__':
    unittest.main()
