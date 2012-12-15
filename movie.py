import os
import json
import urllib2
import re

#stores a list of titles from the local drive
movies_list = []
#dictionary of movies with all details form imdb
movie_dict = {}


limit = 500

#open the directory containing all of the movies.
os.chdir("/Volumes/My_Book/Movies")

#Match this
pattern = "^[A-Za-z0-9' -]+"

#if the last four chars of a string are a number, remove it
def removeTrailingNumber(string):
    last4chars = string[-4:]
    if last4chars.isdigit():
        #remove the string
        return string[:-4]
    else:
        #keep the whole string
        return string


#go through everything in the folder
for files in os.listdir("."):

        matchObj = re.match( pattern , files)

        if matchObj:

            movie = matchObj.group()
            movie = removeTrailingNumber(movie)

            movies_list.append(movie)
            #print "Title: ", movie








#print objs.keys()




#movies_list.append(movie_dict)
#print movies_list


print "%d movies found!" % len(movies_list)

#loop through movies in the list
count = 0
while (count < limit and count < len(movies_list)):

    #print movies_list[count]
    title = movies_list[count].replace(' ','+')
    year = ""

    url = 'http://www.imdbapi.com/?t=%s&y=%s' % (title, year)
    #print url


    error = False
    try:
        data = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
        error = True
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
        error = True

    if not error:
        objs = json.loads(data)

        #Check if it found anything for that search
        if objs[u'Response'] == "True":
            
            #print objs
            movie_dict[objs[u'Title']]     = objs
            #movie_dict['year']      = objs[u'Year']
            #movie_dict['rated']     = objs[u'Rated']
            #movie_dict['score']     = objs[u'imdbRating']
        else:
            #print "Not found!"
            movie_dict[movies_list[count]]     = objs


    count += 1


#Print movies which we found
print "---------------------------------------"
print "Movies which we found data for:\n"
for (current_movie,data) in movie_dict.iteritems():
    if data[u'Response'] == "True":
        print "-- %32s \t\t %s " % (current_movie, data[u'imdbRating'])

print "---------------------------------------"
print "Movies which we found NO data for:\n"
#Print movies which couldn't be found
for (current_movie,data) in movie_dict.iteritems():
    if data[u'Response'] == "False":
        print "-- %32s " % current_movie




