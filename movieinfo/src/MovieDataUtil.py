import logging

class MovieDataUtil:

    def sortMovieData(self, movieData):
        """sort our movie dictionary by their IMDB rating value."""
        movieData = sorted(movieData.iteritems(), reverse=True, key=lambda (k,v): (v['imdbRating'],k))
        return movieData

    def isValidLookupResult(self, movieData):
        if movieData['Response']  == "True": #probably not the best way to check this...
            return True
        return False
