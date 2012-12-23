import os
import json
import urllib2
import re

#####################################################
#Settings
#####################################################
#The directory where your movies are stored
#They can be files or folders within that dir
#MOVIE_DIR = "/Volumes/My_Book/Movies"
MOVIE_DIR = "/Users/kim/Downloads/complete/Movies"

#The maximum number of movies to search through
#Use a small number for testing, default: 1000
LIMIT = 1000

#True for fancy HTML output
#False for simple output with only the rating
HTML_OUTPUT = False

#Match this regex pattern
movie_match_regex = "^[A-Za-z0-9' -]+"
#####################################################




#stores a list of titles from the local drive
movies_list = []

#dictionary of movies with all details from IMDB
#key is the title
#value is the list of attributes from IMDB
movie_dict = {}

#structure for storing movies which we couldn't find
not_found_dict = {}

#open the directory containing all of the movies.
os.chdir(MOVIE_DIR)



#If the last four chars of a string are a number, remove it
#This might cause a problem with some movies...
def removeTrailingNumber(string):
    last4chars = string[-4:]
    if last4chars.isdigit():
        #remove the string
        return string[:-4]
    else:
        #keep the whole string
        return string


#go through everything in the current folder
for files in os.listdir("."):

        #Match our regex against everything in the folder
        matchObj = re.match( movie_match_regex , files)


        #Add all items which matched the pattern to our list to lookup later
        if matchObj:

            movie = matchObj.group()
            movie = removeTrailingNumber(movie)

            movies_list.append(movie)
            #print "Title: ", movie



print "%d items matched in directory!" % len(movies_list)

#Loop through the potential movies in the list
count = 0   #keep a count of the number of items we have checked...
while (count < LIMIT and count < len(movies_list)):

    #print movies_list[count]

    #Replace spaces with a + (so it's a valid url)
    title = movies_list[count].replace(' ','+')
    #Get the year using the regex later if needed (it seems to be quite successful without it)
    year = ""

    #Generate the URL of the api lookup for each movie title
    url = 'http://www.imdbapi.com/?t=%s&y=%s' % (title, year)
    #print url


    #Try and get a json response from the URL...
    error = False
    try:
        data = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
        error = True
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
        error = True

    #It looks like the lookup returned something...
    if not error:
        json_movie_data = json.loads(data)

        #Check if it found anything useful
        if json_movie_data[u'Response'] == "True":
            
            #print "A movie was found!"
            #print objs
            movie_dict[json_movie_data[u'Title']]     = json_movie_data
            #json_movie_data keys include: imdbRating, title, year, rated, released, director...

        else:
            #print "This movie was not found!"
            not_found_dict[movies_list[count]]     = json_movie_data
    
    else:
        print "Fatal Error, can not continue!"
        break;


    count += 1

#####################################################
#Output
#####################################################
if HTML_OUTPUT:
    print "<html>"

#Do the simple output
else:
    #Print movies which we found
    print "---------------------------------------"
    print "Movies which we found data for:\n"
    for (current_movie,data) in movie_dict.iteritems():
            print "-- %32s \t\t %s " % (current_movie, data[u'imdbRating'])

    print "---------------------------------------"
    print "Items which we found NO data for:\n"
    #Print movies which couldn't be found
    for (current_movie,data) in not_found_dict.iteritems():
            print "-- %32s " % current_movie
    print "---------------------------------------"
    print "Done."




