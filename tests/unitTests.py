import unittest
import sys

#import the program
sys.path.append(".")
from movie import *

class TestSequenceFunctions(unittest.TestCase):

    allowedFiletypes = ["tmp","avi","mpg","mpeg","mkv","mp4","divx"]
    matchRegex = "^[^.].+$"

    def setUp(self):
        self.matcher = Matcher(self.matchRegex, self.allowedFiletypes)

    #####################################################
    #Test the Matcher Class
    #####################################################

    def testFileExtensionValidation(self):
        is_valid_extension = self.matcher._isValidExtension("avi")
        self.assertTrue(is_valid_extension)

    def testFindInDirectory(self):
        directory = "./tests/testMovieDirectory"
        self.matcher.findInDirectory(directory)

        movieMatches = self.matcher.getMatches()
        unMatched = self.matcher.getIgnored()

        numberOfMatches = len(movieMatches)
        numberOfNonMatches = len(unMatched)

        self.assertEquals(numberOfMatches, 8)
        self.assertEquals(numberOfNonMatches, 1)

    #####################################################


if __name__ == '__main__':
    unittest.main()