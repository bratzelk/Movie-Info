import unittest

import sys
import os
import inspect

#import the program from the src directory
pathname = os.path.dirname(sys.argv[0])

sys.path.append(os.path.join(os.path.abspath(pathname), '..', 'src'))
from main import *


class TestSequenceFunctions(unittest.TestCase):

    allowedFiletypes = ["tmp","avi","mpg","mpeg","mkv","mp4","divx"]
    matchRegex = "^[^.].+$"

    def setUp(self):
        self.matcher = Matcher(self.matchRegex, self.allowedFiletypes)
        self.movieLookUp = MovieLookUp()
        self.normaliser = Normaliser()



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

        self.assertEquals(numberOfMatches, 10)
        self.assertEquals(numberOfNonMatches, 1)

    #####################################################




    #####################################################
    #Test the MovieLookUp Class
    #####################################################

    def testEmptyByDefault(self):
        foundMovies = self.movieLookUp.getFoundMovieData()
        numberOfItems = len(foundMovies)
        self.assertEquals(numberOfItems, 0)

    #####################################################


if __name__ == '__main__':
    unittest.main()