#!/usr/bin/env python
"""
---------------------------------------
Movie Info
By Kim Bratzel 2014
---------------------------------------
"""

import sys
import socket
import argparse
import time
import logging

from jinja2 import Environment, FileSystemLoader

from movieinfo.src.Matcher import Matcher
from movieinfo.src.MovieLookup import MovieLookup
from movieinfo.src.MovieDataUtil import MovieDataUtil
from movieinfo.src.Normaliser import Normaliser
from movieinfo.src.IdFinder import IdFinder
from movieinfo.src.Cache import Cache

from movieinfo.src.Config import Config


__version__ = "0.7"
__author__ = "Kim Bratzel"

__movielookup__ = MovieLookup()

#Match files in a given directory
__matcher__ = Matcher(Config.movie_match_regex, Config.allowed_file_types)

#Used to find an imdb id from movie filename
__id_finder__ = IdFinder()

#Used for caching movie data
__movie_cache__ = Cache(Config.movie_cache_file)

def simple_output(movie_lookup_data, failed_lookups, unmatched):
    """Produces some simple output"""

    print "---------------------------------------"
    print "Movie Info By Kim Bratzel (Simple Output)"
    print "---------------------------------------"
    print "%d item(s) matched in directory!" % (len(movie_lookup_data) +
                                                len(failed_lookups))
    print "%d movie(s) which we found!" % len(movie_lookup_data)
    print "%d movie(s) which we couldn't find!" % len(failed_lookups)
    print "%d file(s) which we totally ignored!" % len(unmatched)

    #Print movies which we found
    print "---------------------------------------"
    print "Movies which we found data for:\n"
    #The second part of this sorts in order of highest IMDB rating
    for data in movie_lookup_data:
        print "-- %32s \t\t %s " % (data['Title'], data['imdbRating'])

    print "---------------------------------------"
    print "Items which we found NO data for:\n"
    #Print movies which couldn't be found
    for title in failed_lookups:
        print "-- %32s " % title
    print "---------------------------------------"

    print "Items which we ignored:\n"
    #Print movies which couldn't be found
    for ignored in unmatched:
        print "-- %32s " % ignored
    print "---------------------------------------"

def lookup_movie_data(normalised_movie_matches, html_output_flag, limit, unmatched):
    """This Looksup the movie data"""

    #Now we lookup successful matches, first in the cache, then online
    movie_data = {}      #successful lookup data will go here
    failed_lookups = []  #we will do something with failed lookups later...

    count = 0   #used to limit the number of lookups we will do
    for title in normalised_movie_matches:
        count += 1
        if count >= limit:#check that we don't go over the arbitrary limit
            break

        #Check if the movie is in our cache
        cached_movie = __movie_cache__.get(title)
        if cached_movie:
            movie_data[title] = cached_movie
        #Otherwise, lookup using API
        else:
            #look up each movie in the list
            lookup_data = __movielookup__.lookup_by_title(title)

            #check if we found a movie
            if MovieDataUtil.is_valid_lookup_result(lookup_data):
                movie_data[title] = lookup_data
                #great, let's also add it to the cache
                __movie_cache__.add_to_cache(title, lookup_data)
            else:
                failed_lookups.append(title)

    #now we will try to correct the failed lookups
    #by using google to find each imdb id
    id_lookup_dict = __id_finder__.find_id_by_title_list(failed_lookups)

    correct_failed_lookups(id_lookup_dict, movie_data, html_output_flag, unmatched)

def correct_failed_lookups(id_lookup_dict, movie_data, html_output_flag, unmatched):
    """Try to correct the titles on failed lookups"""

    #reset the failed lookups
    failed_lookups = []      #there should be a lot less now...
    title_corrections = 0    #count how many corrections we actually found

    #Now lookup using the new ids which we found
    for title, found_id in id_lookup_dict.items():
        if found_id != None:
            #we found an id, now let's look the movie up by its id
            lookup_data = __movielookup__.lookup_by_id(found_id)

            #theoretically this should always be true
            #unless we got an invalid id somehow...
            if MovieDataUtil.is_valid_lookup_result(lookup_data):
                movie_data[title] = lookup_data
                title_corrections += 1
                #great, let's also add it to the cache
                __movie_cache__.add_to_cache(title, lookup_data)
            else:
                failed_lookups.append(title)
        else:
            failed_lookups.append(title)

    #sort the data by imdb id
    movie_data = MovieDataUtil.sort_movie_data(movie_data)

    #Output the data
    if html_output_flag:
        logging.debug('Loading template from: %s', Config.template_directory)
        template_environment = Environment( \
                        loader=FileSystemLoader( \
                        Config.template_directory), trim_blocks=True)
        print template_environment.get_template('main.html').render(
            movie_lookup_data=movie_data,
            failed_lookups=failed_lookups,
            unmatched=unmatched,
            title_corrections=title_corrections,
            datetime=time.strftime("%c"),
            version=__version__,
            author=__author__,
            cache_stats=__movie_cache__.cache_stats(),
        )
    else:
        simple_output(movie_data, failed_lookups, unmatched)

def run(movie_dir, html_output_flag, limit):
    """This is the real entry point for the program"""

    #First, let's match files which match the regex and have the
    #required file extensions in the given directory
    __matcher__.find_in_directory(movie_dir)
    movie_matches = __matcher__.get_matches()
    unmatched = __matcher__.get_ignored()

    #normalise the matches (the filenames will be used as movie titles)
    normalised_movie_matches = Normaliser\
        .normalise_and_remove_number(movie_matches)

    lookup_movie_data(normalised_movie_matches, html_output_flag, limit, unmatched)

    #Save the updated cache
    __movie_cache__.save_cache_to_disk()

#####################################################
def start():
    """Runner to set up cmd args and start the program"""

    #Set up the command line arguments
    parser = argparse.ArgumentParser(description='Movie Info')
    parser.add_argument('-dir', '-d', required=True, \
                       help='The directory where your movies are stored')
    parser.add_argument('-limit', '-l', type=int, nargs='?', \
                        default=1000, required=False, \
                        help='The maximum number of movies to search through')
    parser.add_argument('-html', '-o', default=False, required=False, \
                        action='store_true', help='Output in HTML')
    parser.add_argument('-v', '-version', action='version', \
                        version='%s'%(__version__))
    args = vars(parser.parse_args())

    #set the timeout
    socket.setdefaulttimeout(Config.timeout)

    #Run the program using the cmd line arguments
    run(args['dir'], args['html'], args['limit'])

    return 0 #success


#####################################################
if __name__ == '__main__':
    #Run the program
    sys.exit(start())
