"""Find metadata for a movie"""

import json
import urllib2
import logging

class MovieLookup(object):
    """Find metadata for a movie"""

    @classmethod
    def _get_api_url(cls, title, year=""):
        """Returns the API URL for a given title"""

        #You could change API quite easily if you find a better one...
        return "http://www.omdbapi.com/?t=%s&y=%s" % (title, year)

    @classmethod
    def _get_api_id_url(cls, imdb_id):
        """Returns the API URL for a given IMDB ID"""

        return "http://www.omdbapi.com/?i=%s" % (imdb_id)

    @classmethod
    def _space_to_plus(cls, title):
        """Replaces spaces with plus to create well formed URLS"""

        return title.replace(' ', '+')

    @classmethod
    def _get_data_from_url(cls, url):
        """Returns the JSON Lookup Data"""
        try:
            lookup_data = urllib2.urlopen(url).read()
        except urllib2.HTTPError, error:
            print "HTTP error: %d" % error.code
            exit()
        except urllib2.URLError, error:
            print "Network error: %s" % error.reason
            exit()

        #It looks like the lookup returned something...
        json_lookup_data = json.loads(lookup_data, encoding="utf-8")

        return json_lookup_data


    def lookup_by_title(self, title):
        """Get metadata for a movie given its title"""

        #Replace spaces with a + (so it's a valid url)
        title = self._space_to_plus(title)

        url = self._get_api_url(title)
        lookup_result = self._get_data_from_url(url)
        return lookup_result

    def lookup_by_id(self, imdb_id):
        """Get metadata for a movie given its IMDB id"""

        url = self._get_api_id_url(imdb_id)
        lookup_result = self._get_data_from_url(url)
        return lookup_result

