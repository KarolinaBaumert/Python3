import unittest
from Zadanie1 import word_frequencies

class MyTestCase(unittest.TestCase):
    def test_word_frequencies(self):
        self.assertEqual(word_frequencies("Hello world hello"), {'hello': 2, 'world': 1})
        self.assertEqual(word_frequencies("This is a test. A test it is."), {'this': 1, 'is': 2, 'a': 2, 'test': 2, 'it': 1})
        self.assertEqual(word_frequencies(""), {})


if __name__ == '__main__':
    unittest.main()
