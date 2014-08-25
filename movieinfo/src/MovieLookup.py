import json
import urllib2
import logging

class MovieLookup(object):

    #I'm using this api for now, but you could change this potentially...
    def _getApiUrl(self, title, year=""):
        return "http://www.omdbapi.com/?t=%s&y=%s" % (title, year)

    def _getApiIdUrl(self, imdbId):
        return "http://www.omdbapi.com/?i=%s" % (imdbId)

    def _makeUrlFriendlyTitle(self, title):
        return title.replace(' ','+')

    def _doLookup(self, url):
        """Returns the JSON Lookup Data"""
        try:
            lookupData = urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            exit()
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason
            exit()

        #It looks like the lookup returned something...
        jsonLookupData = json.loads(lookupData, encoding="utf-8")

        return jsonLookupData


    def lookupByTitle(self, title):

        #Replace spaces with a + (so it's a valid url)
        title = self._makeUrlFriendlyTitle(title)

        url = self._getApiUrl(title)
        lookupResult = self._doLookup(url)
        return lookupResult

    def lookupById(self, imdbId):
        url = self._getApiIdUrl(imdbId)
        lookupResult = self._doLookup(url)
        return lookupResult

