import pickle
import os

class Cache:
    """This class caches looked up movies in order to improve efficiency. """

    #This is the name of the file where the cache is stored
    cacheFile = "cache.p"


    def __init__(self):

        """If the cache file doesn't exist then create it"""
        if not os.path.exists(self.cacheFile):
            open(self.cacheFile, 'w').close() 

    def saveToCache(self, data, cacheFile):
        pickle.dump(data, open(cacheFile, "wb"))

    def getFromCache(self, cacheFile):
        data = pickle.load(open(cacheFile, "rb"))
        return data