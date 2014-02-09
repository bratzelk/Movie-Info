import json
import re
import urllib
import urllib2



#This class will find an IMDB Movie id given a movie title
#It can be used to help correct erroneous movie titles
class IMDBIdFinder:

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


    def lookupSingleName(self, name):

        lookupSite = self._lookupSite(name)

        searchURL = lookupSite["searchURL"]

        results = json.load(urllib.urlopen(searchURL))
        try:
            url = results['responseData']['results'][0]['url']
            IMDBId = re.search(lookupSite["urlparser"], url).group(1)
        except:
            IMDBId = "none"

        return IMDBId

    def lookupManyNames(self, namesList):
        idList = []
        for name in namesList:
            idList.append(self.lookupSingleName(name))
        return idList


