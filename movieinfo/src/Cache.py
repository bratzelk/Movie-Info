"""This is a generic key/value cache which saves data to a file."""

import pickle
import os
import logging

class Cache(object):
    """This is a generic key/value cache which saves data to a file."""

    #The current working directory
    _cache_dir = os.getcwd()

    #This is the name of the file where the movie cache is stored
    _cache_file = ""

    _cache_data = {}
    _dirty = False

    _hits = 0
    _misses = 0


    def __init__(self, _cache_file):
        """Load a cache from a file, create it if the file doesn't exist."""
        self._set_cache_file(_cache_file)

        #If the cache file doesn't exist then create it.
        if not os.path.exists(self._get_cache_file()):
            logging.debug('Pickle cache does not exist. Create a new one.')
            logging.debug('Cache file will be saved in: %s', self._cache_dir)
            open(self._get_cache_file(), 'w').close()

        self._cache_data = self._get_data_from_cache()

    def _get_data_from_cache(self):
        """Get dictionary data from any cache file"""
        logging.debug('Loading data from cache file: %s', self._cache_file)
        try:
            data = pickle.load(open(self._cache_file, "rb"))
            return data
        except EOFError:
            return {}

    def _set_cache_file(self, _cache_file):
        """Set the cache file to use"""
        self._cache_file = os.path.join(self._cache_dir, _cache_file)

    def _get_cache_file(self):
        """Get the cache file"""
        return self._cache_file

    def delete_cache(self):
        """Delete the Cache File"""
        logging.debug('Deleting entire cache file')
        try:
            os.remove(self._get_cache_file())
        except OSError:
            pass

        self._cache_data = {}
        self._hits = 0
        self._misses = 0
        self._dirty = False

    def get(self, item):
        """Returns the item in the Cache or None if item is not found"""
        result = self._cache_data.get(item)
        if result:
            self._hits += 1
            logging.debug('Cache hit for: %s', item)
        else:
            self._misses += 1
            logging.debug('Cache miss for: %s', item)

        return result

    def add_to_cache(self, key, value):
        """Add data to the cache. Will overwrite anything currently in the
         cache with the same key. This won't be saved to disk."""
        self._cache_data[key] = value
        self._dirty = True

    def is_dirty(self):
        """Has the cache been updated"""
        return self._dirty

    def save_cache_to_disk(self):
        """Update the cache on disk"""
        if self._dirty:
            logging.debug('Cache dirty, saving to disk.')
            pickle.dump(self._cache_data, open(self._cache_file, "wb"))
            self._dirty = False
        else:
            logging.debug('Cache clean, not actually saving.')

    def get_hits(self):
        """Returns the number of cache hits"""
        return self._hits

    def get_misses(self):
        """Returns the number of cache misses"""
        return self._misses

    def get_cache_size(self):
        """Returns the number of entries in the cache"""
        return len(self._cache_data)

    def cache_stats(self):
        """Returns some cache stats"""
        return  {\
            "hits": self.get_hits(), \
            "misses": self.get_misses(), \
            "file": self._get_cache_file(), \
            "size": self.get_cache_size(),
                }

