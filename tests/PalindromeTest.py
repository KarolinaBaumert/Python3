import unittest
from Zadanie1 import is_palindrome

class MyTestCase(unittest.TestCase):
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("kajak"))
        self.assertTrue(is_palindrome("Kobyła ma mały bok"))
        self.assertFalse(is_palindrome("python"))
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome("A"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))


if __name__ == '__main__':
    unittest.main()
