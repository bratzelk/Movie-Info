import unittest

import sys
import os
import inspect

#import the program from the src directory
pathname = os.path.dirname(sys.argv[0])

sys.path.append(os.path.join(os.path.abspath(pathname), '..', 'src'))
from main import *


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.matcher = Matcher(Config.movieMatchRegex, Config.allowedFiletypes)
        self.movieLookup = MovieLookup()
        self.movieDataUtil = MovieDataUtil()
        self.normaliser = Normaliser()
        self.idFinder = IdFinder()


    #####################################################
    #Test the Config Class
    #####################################################
    def testConfigVarsExist(self):
        self.assertGreater(Config.timeout, 0)
        self.assertGreater(len(Config.allowedFiletypes), 0)

    def testConfigVarsNotExist(self):
        with self.assertRaises(AttributeError):
            print Config.fake

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

        self.assertEquals(numberOfMatches, 11)
        self.assertEquals(numberOfNonMatches, 1)

    #####################################################



    #####################################################
    #Test the MovieLookup Class
    #####################################################
    def testBadMovieLookup(self):
        title = "Film Does Not Exist"
        lookupResult = self.movieLookup.lookupByTitle(title)
        isValidLookup = self.movieDataUtil.isValidLookupResult(lookupResult)
        self.assertFalse(isValidLookup)

    def testGoodMovieLookup(self):
        title = "true grit"
        lookupResult = self.movieLookup.lookupByTitle(title)
        isValidLookup = self.movieDataUtil.isValidLookupResult(lookupResult)
        self.assertTrue(isValidLookup)
    #####################################################


    #####################################################
    #Test the IdFinder Class
    #####################################################
    def testFindKnownMovie(self):
        knownId = "tt0105793"
        lookupId = self.idFinder.find_id_by_title("Waynes World 1992")
        self.assertEquals(lookupId, knownId)

    def testFindNonExistantMovie(self):
        lookupId = self.idFinder.find_id_by_title(" !!^&*#@ Some fake film title...")
        self.assertIsNone(lookupId)


    #####################################################
    #Integration Tests
    #####################################################

    def testIdFindAndMovieLookup(self):
        """
        Lookup a movie with an incorrect title,
        Find the IMDB id for this movie,
        Find the correct title
        """
        title = "Waynes world 2"
        actualTitle = "Wayne's World 2"

        lookupResult = self.movieLookup.lookupByTitle(title)
        isValidLookup = self.movieDataUtil.isValidLookupResult(lookupResult)
        #Check that this isn't a correct title (it is missing an apostrophe)
        self.assertFalse(isValidLookup)

        foundId = self.idFinder.find_id_by_title(title)
        #check that we found an id for this movie
        self.assertIsNotNone(foundId)

        lookupResult = self.movieLookup.lookupById(foundId)
        isValidLookup = self.movieDataUtil.isValidLookupResult(lookupResult)
        self.assertTrue(isValidLookup)

        #now check the new title compares to the actual title
        self.assertEquals(lookupResult['Title'], actualTitle)


if __name__ == '__main__':
    unittest.main()
