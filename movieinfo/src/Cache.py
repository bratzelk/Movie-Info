import pickle
import os
import logging

class Cache:
    """This class caches looked up movies in order to improve efficiency. """

    #The current working directory
    cacheDir = os.getcwd()

    #This is the name of the file where the movie cache is stored
    cacheFile = ""

    cacheData = {}
    dirty = False

    hits = 0
    misses = 0


    def __init__(self, cacheFile):
        """Load a cache from a file, create it if the file doesn't exist."""
        self._setCacheFile(cacheFile)

        #If the cache file doesn't exist then create it.
        if not os.path.exists(self._getCacheFile()):
            logging.debug('Pickle cache does not exist. Create a new one.')
            logging.debug('Cache file will be saved in: %s', self.cacheDir)
            open(self._getCacheFile(), 'w').close()

        self.cacheData = self._getDataFromCache(self._getCacheFile())

    def _deleteCacheFile(self, cacheFile):
        os.remove(cacheFile)

    def _getDataFromCache(self, cacheFile):
        """Get dictionary data from any cache file"""
        logging.debug('Loading data from cache file: %s', self.cacheFile)
        try:
            data = pickle.load(open(cacheFile, "rb"))
            return data
        except EOFError:
            return {}

    def _setCacheFile(self, cacheFile):
        """Set the cache file to use"""
        self.cacheFile = os.path.join(self.cacheDir, cacheFile)

    def _getCacheFile(self):
        """Get the cache file"""
        return self.cacheFile

    def deleteCache(self):
        """Delete the Cache File"""
        logging.debug('Deleting entire cache file')
        self._deleteCacheFile(self._getCacheFile())

    def find(self, item):
        """Returns the item in the Cache or None if item is not found"""
        result = self.cacheData.get(item)
        if(result):
            self.hits += 1
            logging.debug('Cache hit for: %s', item)
        else:
            self.misses += 1
            logging.debug('Cache miss for: %s', item)

        return result

    def addToCache(self, key, value):
        """Add data to the cache. Will overwrite anything currently in the cache with the same key. This won't be saved to disk."""
        self.cacheData[key] = value
        self.dirty = True

    def isDirty(self):
        """Has the cache been updated"""
        return self.dirty

    def saveCacheToDisk(self):
        """Update the cache on disk"""
        if(self.dirty):
            logging.debug('Cache dirty, saving to disk.')
            pickle.dump(self.cacheData, open(self.cacheFile, "wb"))
            self.dirty = False
        else:
            logging.debug('Cache clean, not actually saving.')

    def hits(self):
        return self.hits

    def misses(self):
        return self.misses

