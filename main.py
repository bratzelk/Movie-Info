#####################################################
#Movie Info 0.5
#By Kim Bratzel 2014
#####################################################

import os
import socket
import argparse
import time

from jinja2 import Environment, FileSystemLoader

from Matcher import Matcher
from MovieLookUp import MovieLookUp
from Normaliser import Normaliser

#####################################################
#Some Settings
#####################################################

#the amount of time to wait before timing out during each lookup
timeout = 5

#a list of filetypes to match (it will also match directory names)
#these are case insensitive
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

