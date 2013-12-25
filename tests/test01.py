import unittest
import sys

#import the program
sys.path.append(".")
from movie import *

class TestSequenceFunctions(unittest.TestCase):

    allowedFiletypes = ["tmp","avi","mpg","mpeg","mkv"]
    matchRegex = "^[^.].+$"

    def setUp(self):
        self.matcher = Matcher(self.matchRegex, self.allowedFiletypes)

    def test_file_extension(self):
        is_valid_extension = self.matcher._isValidExtension("avi")
        self.assertTrue(is_valid_extension)


if __name__ == '__main__':
    unittest.main()