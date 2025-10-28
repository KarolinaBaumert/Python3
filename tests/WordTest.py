import unittest
from Zadanie1 import word_frequencies

class MyTestCase(unittest.TestCase):
    def test_word_frequencies(self):
        self.assertEqual(word_frequencies("To be or not to be"), {'to': 2, 'be': 2, 'or': 1, 'not': 1})
        self.assertEqual(word_frequencies("Hello, hello!"), {'hello': 2})
        self.assertEqual(word_frequencies(""), {})
        self.assertEqual(word_frequencies("Python Python python"), {'python': 3})
        self.assertEqual(word_frequencies("Ala ma kota, a kot ma Ale."), {'ala': 1, 'ma': 2, 'kota': 1, 'a': 2, 'kot': 1, 'ale': 1})


if __name__ == '__main__':
    unittest.main()
