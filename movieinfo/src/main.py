#####################################################
#Movie Info
#By Kim Bratzel 2014
#####################################################

import sys
import os
import socket
import argparse
import time
import logging

from jinja2 import Environment, FileSystemLoader

from Matcher import Matcher
from MovieLookup import MovieLookup
from MovieDataUtil import MovieDataUtil
from Normaliser import Normaliser
from IdFinder import IdFinder
from Cache import Cache


__version__ = "0.6"


#####################################################
#Some Settings
#####################################################

#Logger Settings
logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#the amount of time to wait before timing out during each lookup
timeout = 20

#a list of filetypes to match (it will also match directory names)
allowedFiletypes = ["tmp","avi","mpg","mpeg","mkv","mp4","divx"]

#The regex pattern used to match movie names
movieMatchRegex = "^[^.].+$"

#The directory where the html templates are stored
templateDirectory = os.path.dirname(os.path.abspath(__file__)) + "/templates"


#####################################################

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
            print "-- %32s \t\t %s " % (data['Title'], data['imdbRating'])

    print "---------------------------------------"
    print "Items which we found NO data for:\n"
    #Print movies which couldn't be found
    for title in failedLookups:
            print "-- %32s " % title
    print "---------------------------------------"

    print "Items which we ignored:\n"
    #Print movies which couldn't be found
    for ignored in unMatched:
            print "-- %32s " % ignored
    print "---------------------------------------"


#####################################################
#The most important bits
#####################################################
def run(MOVIE_DIR, HTML_OUTPUT_FLAG, LIMIT):

    movielookup = MovieLookup()                         #A class to help lookup movie titles
    movieDataUtil = MovieDataUtil()                     #A helper class for movie json data
    matcher = Matcher(movieMatchRegex, allowedFiletypes)#Match files in a given directory
    normaliser = Normaliser()                           #
    idFinder = IdFinder()                               #Used to find an imdb id from movie filename
    cache = Cache()                                     #Used for caching data

    #First, let's match files which match the regex and have the required file extensions in the given directory
    matcher.findInDirectory(MOVIE_DIR)
    movieMatches = matcher.getMatches()
    unMatched = matcher.getIgnored()

    #normalise the matches (the filenames will be used as movie titles)
    normalisedMovieMatches = []
    for item in movieMatches:
        normalisedItem = item
        normalisedItem = normaliser.removeTrailingNumber(normalisedItem)
        normalisedItem = normaliser.normalise(normalisedItem)
        normalisedMovieMatches.append(normalisedItem)

    #Now we lookup successful matches, first in the cache, then online
    movieData = {}      #successful lookup data will go here
    failedLookups = []  #we will do something with failed lookups later...
    cachedMovies = cache.getMovieData() #the previously found movies

    count = 0   #used to limit the number of lookups we will do
    for title in normalisedMovieMatches:
        count += 1
        if count >= LIMIT:#check that we don't go over the arbitrary limit
            break

        #Check if the movie is in our cache
        if(cachedMovies.get(title)):
            movieData[title] = cachedMovies.get(title)
        #Otherwise, lookup using API
        else:
            #look up each movie in the list
            lookupData = movielookup.lookupByTitle(title)

            #check if we found a movie
            if movieDataUtil.isValidLookupResult(lookupData):
                movieData[title] = lookupData
                #great, let's also add it to the cache
                cachedMovies[title] = lookupData
            else:
                failedLookups.append(title)

    #now we will try to correct the failed lookups by using google to find each imdb id
    idLookupDict = idFinder.findIdByTitleList(failedLookups)

    #reset the failed lookups
    failedLookups = []      #there should be a lot less now...
    titleCorrections = 0    #count how many corrections we actually found

    #Now lookup using the new ids which we found
    for title, foundId in idLookupDict.items():
        if foundId != None:
            #we found an id, now let's look the movie up by its id
            lookupData = movielookup.lookupById(foundId)

            #theoretically this should always be true unless we got an invalid id somehow...
            if movieDataUtil.isValidLookupResult(lookupData):
                movieData[title] = lookupData
                titleCorrections += 1
                #great, let's also add it to the cache
                cachedMovies[title] = lookupData
            else:
                failedLookups.append(title)
        else:
            failedLookups.append(title)

    #Save the updated cache
    cache.saveMovieData(cachedMovies)

    #sort the data by imdb id
    movieData = movieDataUtil.sortMovieData(movieData)

    #Output the data
    if HTML_OUTPUT_FLAG:
        logging.debug('Loading template from: %s', templateDirectory)
        templateEnvironment = Environment(loader=FileSystemLoader(templateDirectory),trim_blocks=True)
        print templateEnvironment.get_template('main.html').render(
            movieLookupData=movieData,
            failedLookups=failedLookups,
            unMatched=unMatched,
            titleCorrections=titleCorrections,
            dateTime = time.strftime("%c"),
            version = __version__,
        )
    else:
        simpleOutput(movieData, failedLookups, unMatched)

#####################################################
#Main Function
#####################################################
def start():

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
    parser.add_argument('-v','-version', action='version', version='%s'%(__version__))
    args = vars(parser.parse_args())
    #####################################################

    #set the timeout
    socket.setdefaulttimeout(timeout)

    #Run the program using the line arguments
    run(args['dir'], args['html'], args['limit'])

    return 0 #success

#####################################################
#Run the program
#####################################################
if __name__ == '__main__':
    status = start()
    sys.exit(status)
