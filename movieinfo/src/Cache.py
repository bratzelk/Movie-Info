import pickle
import os
import logging

class Cache:
    """This class caches looked up movies in order to improve efficiency. """

    #The current working directory
    cacheDir = os.getcwd()

    #This is the name of the file where the movie cache is stored
    cacheFile = os.path.join(cacheDir, "movieCache.p")


    def __init__(self):
        """If the cache file doesn't exist then create it"""
        if not os.path.exists(self.getMovieCacheFile()):
            logging.debug('Pickle cache does not exist. Create a new one.')
            logging.debug('Cache file will be saved in: %s', self.cacheDir)
            open(self.getMovieCacheFile(), 'w').close() 

    def _saveToCache(self, data, cacheFile):
        """Save any dictionary to a cache file"""
        pickle.dump(data, open(cacheFile, "wb"))

    def _getDataFromCache(self, cacheFile):
        """Get dictionary data from any cache file"""
        try:
            data = pickle.load(open(cacheFile, "rb"))
            return data
        except EOFError:
            return {}

    def _deleteCacheFile(self, cacheFile):
        os.remove(cacheFile)

    def getMovieCacheFile(self):
        """Get the movie cache file"""
        return self.cacheFile

    def getMovieData(self):
        """Return the movie data from the cache file"""
        return self._getDataFromCache(self.getMovieCacheFile())

    def saveMovieData(self, movieData):
        """Save the movie data to the cache file"""
        self._saveToCache(movieData, self.getMovieCacheFile())

    def deleteMovieCache(self):
        """Delete the movie cache file"""
        self._deleteCacheFile(self.getMovieCacheFile())