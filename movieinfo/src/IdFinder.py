import json
import re
import urllib
import urllib2
import logging
import time


#This class will find an IMDB Movie id given a movie title
#It can be used to help correct erroneous movie titles
class IdFinder:

    def __init__(self):
        pass

    def _lookupSite(self, title):

        domain = "imdb.com"
        urlparser = "imdb.com/title\/(.*?)\/"
        #searchURL = "http://www.google.com/search?q=site%%3A%s+%s" % (domain, title)
        searchURL = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=site%%3A%s+%s" % (domain, title)
        return  {
                    "domain": domain,
                    "urlparser": urlparser,
                    "searchURL": searchURL,
                }

    def findIdByTitle(self, title):
        """ """

        #let's limit the number of requests to 0.5/second to avoid sending too many requests
        time.sleep(2)

        logging.debug('Searching Google/IMDB for: %s', title)
        lookupSite = self._lookupSite(title)
        searchURL = lookupSite["searchURL"]
        results = json.load(urllib.urlopen(searchURL))
        try:
            url = results['responseData']['results'][0]['url']
            IMDBId = re.search(lookupSite["urlparser"], url).group(1)
            logging.debug('IMDB ID found: %s', IMDBId)
        except:
            IMDBId = None
            logging.debug('IMDB ID not found!')

        return IMDBId

    def findIdByTitleList(self, titleList):
        idDict = {}
        for title in titleList:
            idDict[title] = self.findIdByTitle(title)
        return idDict


