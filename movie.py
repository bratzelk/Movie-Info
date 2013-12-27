#####################################################
#Movie Info 0.5
#By Kim Bratzel 2014
#####################################################

import os
import json
import urllib2
import socket
import re
import argparse
import time

from jinja2 import Environment, FileSystemLoader

#####################################################
#Some Settings
#####################################################

#the amount of time to wait before timing out during each lookup
timeout = 5

#a list of filetypes to match (it will also match directory names)
#these are case insensitive
allowedFiletypes = ["tmp","avi","mpg","mpeg","mkv"]

#The regex pattern used to match movie names
movieMatchRegex = "^[^.].+$"

#The directory where the html templates are stored
templateDirectory = os.path.dirname(os.path.abspath(__file__)) + "/templates"

#####################################################

class Normaliser:
    def __init__(self):
        pass

    #If the last four chars of a string are a number, remove them
    #This might cause a problem with some movies...
    def removeTrailingNumber(self, string):
        last4chars = string[-4:]
        if last4chars.isdigit():
            #remove the string
            return string[:-4]
        else:
            #keep the whole string
            return string

    def normalise(self, string):
        return string.lower()

    def normaliseList(self, list):
        newList = []
        for item in list:
            newList.append(self.normalise(item))

#This creates a list of directories and filenames which match a regex within a single directory
#it creates a list of matched filenames/directories and list of ignored, or unmatched filenames/directories
class Matcher:

    #stores a list of titles from the local drive which were match in the given directory
    matchList = []
    #A list of items which were ignored due to their file extension (not really used for anything)
    ignoredList = []

    def __init__(self, matchRegex,allowedFiletypes):
        self.matchList = []
        self.ignoredList = []

        self.matchRegex = matchRegex

        self.allowedFiletypes = allowedFiletypes

    def _addMatch(self, item):
        self.matchList.append(item)

    def _ignore(self, item):
        self.ignoredList.append(item)

    def getMatches(self):
        return self.matchList

    def getIgnored(self):
        return self.ignoredList


    #extract file extension from the filename, if it exists
    def _getFileExtension(self, fullFileName):
        try:
            (filename, extension) = fullFileName.rsplit( ".", 1 )
        except:
            filename = fullFileName
            extension = ""
        return (filename, extension)

    #check if a file extension is in our allowed list
    def _isValidExtension(self, extension):
        #force all lowercase file extensions
        allowedFiletypes = map(lambda x:x.lower(), self.allowedFiletypes)
        if len(extension) in range(1,5) and extension.lower() not in allowedFiletypes:
            return False
        else:
            return True

    #find items in a directory which match our rules
    def findInDirectory(self, directory):
        #open the directory containing all of the matches.
        try: #could also use: os.path.isdir()
            os.chdir(directory)
        except:
            print "Error: Directory, %s does not exist!" % (directory)
            exit()

        #go through everything in the current folder
        for files in os.listdir("."):

            #Match our regex against everything in the folder
            matchObj = re.match( self.matchRegex , files)

            #Add all items which matched the pattern to our list to lookup later
            if matchObj:

                item = matchObj.group()

                (item, extension) = self._getFileExtension(item)

                #if the file extension doesn't exist or is allowed then we add the movie to the list
                if self._isValidExtension(extension):
                    self._addMatch(item)
                    #print item
                else:
                    #print "Ignoring Item: %s" % item
                    self._ignore(item+"."+extension)

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
        return "http://www.imdbapi.com/?t=%s&y=%s" % (title, year)

    def _makeUrlFriendlyTitle(self, title):
        return title.replace(' ','+')

    def lookupTitles(self, movieTitles):

        #Loop through the potential movies in the list
        count = 0   #keep a count of the number of items we have checked...
        while (count < self.limit and count < len(movieTitles)):

            #Replace spaces with a + (so it's a valid url)
            title = self._makeUrlFriendlyTitle(movieTitles[count])

            #Generate the URL of the api lookup for each movie title
            #you could optionally add the year as a second parameter to get better results...
            url = self._getApiUrl(title)

            #Try and get a json response from the URL...
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
                #print "Found Movie: %s" % json_movie_data['Title']
                self._addMovie(jsonLookupData['Title'], jsonLookupData)
                #jsonLookupData keys include: imdbRating, title, year, rated, released, director...
            else:
                #print "Couldn't Find: %s" % title
                self.addNotFoundMovie(movieTitles[count], jsonLookupData)

            count += 1


#####################################################
#Function to produce some simple output
#####################################################
def simpleOutput(movieLookupData, failedLookups, unMatched):
    print "---------------------------------------"
    print "Movie Info By Kim Bratzel (Simple Output)"
    print "---------------------------------------"
    print "%d item(s) matched in directory!" % (len(movieLookupData) + len(failedLookups))
    print "%d movie(s) which we found!" % len(movieLookupData)
    print "%d movie(s) which we couldn't find!" % len(failedLookups)
    print "%d file(s) which we totally ignored!" % len(unMatched)

    #Print movies which we found
    print "---------------------------------------"
    print "Movies which we found data for:\n"
    #The second part of this sorts in order of highest IMDB rating
    for (current_movie,data) in movieLookupData:
            print "-- %32s \t\t %s " % (current_movie, data['imdbRating'])

    print "---------------------------------------"
    print "Items which we found NO data for:\n"
    #Print movies which couldn't be found
    for (current_movie,data) in failedLookups.iteritems():
            print "-- %32s " % current_movie
    print "---------------------------------------"

    print "Items which we ignored:\n"
    #Print movies which couldn't be found
    for (ignored) in unMatched:
            print "-- %32s " % ignored
    print "---------------------------------------"

#####################################################
#Run the program
#####################################################
if __name__ == '__main__':

    #####################################################
    #Set up the command line arguments
    #####################################################
    parser = argparse.ArgumentParser(description='Movie Info')
    parser.add_argument('-dir', '-d', required=True,
                       help='The directory where your movies are stored')
    parser.add_argument('-limit', '-l', type=int, nargs='?', default=1000, required=False,
                       help='The maximum number of movies to search through')
    parser.add_argument('-html','-o', default=False, required=False, action='store_true', 
                       help='Output in HTML')
    parser.add_argument('-v', action='version', version='%(prog)s 0.5')
    args = vars(parser.parse_args())
    #####################################################

    #get our command line arguments as variables
    MOVIE_DIR = args['dir']
    HTML_OUTPUT = args['html']
    LIMIT = args['limit']

    #set the timeout
    socket.setdefaulttimeout(timeout)

    #####################################################

    #Match files in the given directory
    matcher = Matcher(movieMatchRegex, allowedFiletypes)
    matcher.findInDirectory(MOVIE_DIR)

    movieMatches = matcher.getMatches()
    unMatched = matcher.getIgnored()

    #normalise the matches
    normalisedMovieMatches = []
    normaliser = Normaliser()
    for item in movieMatches:
        normalisedItem = item
        normalisedItem = normaliser.removeTrailingNumber(normalisedItem)
        normalisedItem = normaliser.normalise(normalisedItem)
        normalisedMovieMatches.append(normalisedItem)


    #Lookup successful matches
    movielookup = MovieLookUp()
    movielookup.lookupTitles(normalisedMovieMatches)

    movielookup.sortMovieData()

    movieLookupData = movielookup.getFoundMovieData()
    failedLookups = movielookup.getNotFoundMovieData()

    #Output the data
    if HTML_OUTPUT:

        template_env = Environment(loader=FileSystemLoader(templateDirectory),trim_blocks=True)
        
        print template_env.get_template('main.html').render(
            movieLookupData=movieLookupData,
            failedLookups=failedLookups,
            unMatched=unMatched,
            dateTime = time.strftime("%c"),
        )
    else:
        simpleOutput(movieLookupData, failedLookups, unMatched)

