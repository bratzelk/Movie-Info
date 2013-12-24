import unittest
import sys

#import the program
sys.path.append(".")
from movie import *

class TestSequenceFunctions(unittest.TestCase):

    allowed_filetypes = ["tmp","avi","mpg","mpeg","mkv"]
    movie_match_regex = "^[^.].+$"

    def setUp(self):
        self.moviematcher = MovieMatcher(movie_match_regex, allowed_filetypes)

    def test_file_extension(self):
        is_valid_extension = self.moviematcher._isValidExtension("avi")
        self.assertTrue(is_valid_extension)


if __name__ == '__main__':
    unittest.main()