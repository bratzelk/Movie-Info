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

from jinja2 import Environment, FileSystemLoader

#####################################################
#Some Settings
#####################################################

#the amount of time to wait before timing out 
timeout = 5

#a list of filetypes to match (it will also match directory names)
#filetypes = "tmp|avi|mpg|mpeg|mkv"
allowed_filetypes = ["tmp","avi","mpg","mpeg","mkv"]

#The regex pattern used to match movie names
movie_match_regex = "^[^.][A-Za-z0-9\.' -]+$"

#The directory where the html templates are stored
template_directory = os.path.dirname(os.path.abspath(__file__)) + "/templates"

#####################################################

#set the timeout
socket.setdefaulttimeout(timeout)

#Set up the command line arguments
parser = argparse.ArgumentParser(description='Movie Info')
parser.add_argument('-dir', '-d', required=True,
                   help='The directory where your movies are stored')
parser.add_argument('-limit', '-l', type=int, nargs='?', default=1000, required=False,
                   help='The maximum number of movies to search through')
parser.add_argument('-html','-o', default=False, required=False, action='store_true', 
                   help='Output in HTML')
parser.add_argument('-v', action='version', version='%(prog)s 0.5')

args = vars(parser.parse_args())


#get our command line arguments as variables
MOVIE_DIR = args['dir']
HTML_OUTPUT = args['html']
LIMIT = args['limit']



#
class MovieMatcher:

    #stores a list of titles from the local drive which were match in the given directory
    movie_list = []
    #A list of items which were ignored due to their file extension (not really used for anything)
    ignored_movie_list = []

    def __init__(self, regexmatch="^[^.][A-Za-z0-9\.' -]+$",allowedfiletypes=["tmp","avi","mpg","mpeg","mkv"]):
        self.movie_list = []
        self.ignored_movie_list = []

        self.movie_match_regex = regexmatch
        self.allowed_filetypes = allowedfiletypes

    def addMovie(self, movie):
        self.movie_list.append(movie)

    def ignoreMovie(self, movie):
        self.ignored_movie_list.append(movie)

    def getMovieList(self):
        return self.movie_list

    def getIgnoredList(self):
        return self.ignored_movie_list

    def findInDirectory(self, directory):
        #open the directory containing all of the movies.
        #Need to do sanity check here
        os.chdir(directory)

        #go through everything in the current folder
        for files in os.listdir("."):

            #Match our regex against everything in the folder
            matchObj = re.match( movie_match_regex , files.lower())

            #Add all items which matched the pattern to our list to lookup later
            if matchObj:

                movie_title = matchObj.group()

                #extract file extension if it exists
                try:
                    (movie_title, extension) = movie_title.rsplit( ".", 1 )
                except:
                    extension = ""

                #if the file extension does not exist or is allowed we add the movie to the list
                if len(extension) in range(1,5) and extension not in allowed_filetypes:
                    #print "Ignoring Film: %s" % movie_title
                    self.ignoreMovie(movie_title+"."+extension)
                else:
                    movie_title = removeTrailingNumber(movie_title)
                    self.addMovie(movie_title)
                    #print movie_title




#If the last four chars of a string are a number, remove them
#This might cause a problem with some movies...
def removeTrailingNumber(string):
    last4chars = string[-4:]
    if last4chars.isdigit():
        #remove the string
        return string[:-4]
    else:
        #keep the whole string
        return string

def lookupTitleOnIMDB(movies_list):

    #dictionary of movies with all details from IMDB
    #key is the title
    #value is the list of attributes from IMDB
    movie_dict = {}
    
    #structure for storing movies which we couldn't find information on (helpful so you can see why the information wasn't found)
    not_found_dict = {}

    #Loop through the potential movies in the list
    count = 0   #keep a count of the number of items we have checked...
    while (count < LIMIT and count < len(movies_list)):

        #Replace spaces with a + (so it's a valid url)
        title = movies_list[count].replace(' ','+')

        #should probably check for special html chars (& etc) too...

        #Get the year using the regex later if needed (it seems to be quite successful without it)
        year = ""

        #Generate the URL of the api lookup for each movie title
        url = 'http://www.imdbapi.com/?t=%s&y=%s' % (title, year)
        #print url

        #Try and get a json response from the URL...
        try:
            data = urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            exit()
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason
            exit()

        #It looks like the lookup returned something...
        json_movie_data = json.loads(data, encoding="utf-8")
        #print json_movie_data

        #Check if it found anything useful
        if json_movie_data['Response']  == "True": #probably not the best way to check this...
            
            #print "Found Movie: %s" % title
            print "Found Movie: %s" % json_movie_data['Title']
            movie_dict[json_movie_data['Title']]     = json_movie_data
            #json_movie_data keys include: imdbRating, title, year, rated, released, director...

        else:
            print "Couldn't Find: %s" % title
            not_found_dict[movies_list[count]]     = json_movie_data

        count += 1

    #sort our movie dictionary by their IMDB rating value.
    movie_dict = sorted(movie_dict.iteritems(), reverse=True, key=lambda (k,v): (v['imdbRating'],k))

    return (movie_dict, not_found_dict)

#####################################################
#Function to produce some simple output
#####################################################
def simpleOutput(movie_dict, not_found_dict, ignored_movie_list):
    print "---------------------------------------"
    print "Movie Info By Kim Bratzel (Simple Output)"
    print "---------------------------------------"
    print "%d item(s) matched in directory!" % (len(movie_dict) + len(not_found_dict))
    print "%d movie(s) which we found!" % len(movie_dict)
    print "%d movie(s) which we couldn't find!" % len(not_found_dict)
    print "%d file(s) which we totally ignored!" % len(ignored_movie_list)

    #Print movies which we found
    print "---------------------------------------"
    print "Movies which we found data for:\n"
    #The second part of this sorts in order of highest IMDB rating
    for (current_movie,data) in movie_dict:
            print "-- %32s \t\t %s " % (current_movie, data['imdbRating'])

    print "---------------------------------------"
    print "Items which we found NO data for:\n"
    #Print movies which couldn't be found
    for (current_movie,data) in not_found_dict.iteritems():
            print "-- %32s " % current_movie
    print "---------------------------------------"

    print "Items which we ignored:\n"
    #Print movies which couldn't be found
    for (ignored) in ignored_movie_list:
            print "-- %32s " % ignored
    print "---------------------------------------"
    print "Done."

#####################################################
#Run the program
#####################################################
if __name__ == '__main__':

    moviematcher = MovieMatcher(movie_match_regex, allowed_filetypes)
    moviematcher.findInDirectory(MOVIE_DIR)

    movies_list = moviematcher.getMovieList()
    ignored_movie_list = moviematcher.getIgnoredList()

    #print "%d items matched in directory!" % len(movies_list)

    (movie_dict, not_found_dict) = lookupTitleOnIMDB(movies_list)


    #####################################################
    #Output
    #####################################################
    if HTML_OUTPUT:

        template_env = Environment(loader=FileSystemLoader(template_directory),trim_blocks=True)
        
        print template_env.get_template('main.html').render(
            movie_dict=movie_dict,
            not_found_dict=not_found_dict
        )
    else:
        simpleOutput(movie_dict, not_found_dict, ignored_movie_list)

