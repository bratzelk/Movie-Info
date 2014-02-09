import json
import urllib2


class MovieLookUp:

    #dictionary of movies with all details from IMDB
    #key is the title
    #value is the list of attributes from IMDB
    movieData = {}

    #structure for storing movies which we couldn't find information on (helpful so you can see why the information wasn't found)
    notFoundData = {}

    def __init__(self, limit=1000):
        self.limit = limit

    #Sorts the found movie data by the imdb rating value
    #NOTE: lookupTitles() must be called before this can be useful
    def sortMovieData(self):
        #sort our movie dictionary by their IMDB rating value.
        self.movieData = sorted(self.movieData.iteritems(), reverse=True, key=lambda (k,v): (v['imdbRating'],k))

    def _addMovie(self, title, data):
        self.movieData[title] = data

    def addNotFoundMovie(self, title, data):
        self.notFoundData[title] = data

    def getFoundMovieData(self):
        return self.movieData

    def getNotFoundMovieData(self):
        return self.notFoundData

    #I'm using this api for now, but you could change this potentially...
    def _getApiUrl(self, title, year=""):
        return "http://www.omdbapi.com/?t=%s&y=%s" % (title, year)

    def _getApiIdUrl(self, imdbId):
        return "http://www.omdbapi.com/?i=%s" % (imdbId)

    def _makeUrlFriendlyTitle(self, title):
        return title.replace(' ','+')



    #returns {success=bool, data=dict} where bool is True if the lookup was successful and dict contains the data for the lookup
    def _doLookup(self, url):
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

        #Check if it found anything useful
        if jsonLookupData['Response']  == "True": #probably not the best way to check this...
            return {"success":True, "data":jsonLookupData}
        else:
            return {"success":False, "data":None}



    def lookupTitles(self, movieTitles):

        #Loop through the potential movies in the list
        count = 0   #keep a count of the number of items we have checked...
        while (count < self.limit and count < len(movieTitles)):

            #Replace spaces with a + (so it's a valid url)
            title = self._makeUrlFriendlyTitle(movieTitles[count])

            #Generate the URL of the api lookup for each movie title
            #you could optionally add the year as a second parameter to get better results...
            url = self._getApiUrl(title)

            doLookup = self._doLookup(url)
            if doLookup["success"]:
                jsonLookupData = doLookup["data"]
                self._addMovie(jsonLookupData['Title'], jsonLookupData)
                #jsonLookupData keys include: imdbRating, title, year, rated, released, director...
            else:
                self.addNotFoundMovie(movieTitles[count], jsonLookupData)

            count += 1

        def lookupById(self, imdbId):
            url = self._getApiIdUrl(imdbId)
            doLookup = self._doLookup(url)
            
