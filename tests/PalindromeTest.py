import unittest
from Zadanie1 import is_palindrome

class MyTestCase(unittest.TestCase):
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(is_palindrome("Hello World"))
        self.assertTrue(is_palindrome("madam"))
        self.assertTrue(is_palindrome(""))


if __name__ == '__main__':
    unittest.main()
