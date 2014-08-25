"""This is where the application settings are found. """

import os
import logging

class Config(object):
    """This is where the application settings are found. """

    #Logger Settings
    logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG,\
     format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')

    #the amount of time to wait (in ms) before timing out during each lookup
    timeout = 20

    #a list of filetypes to match (it will also match directory names)
    allowed_file_types = ["tmp", "avi", "mpg", "mpeg", "mkv", "mp4", "divx"]

    #The regex pattern used to match movie names
    movie_match_regex = "^[^.].+$"

    #The directory where the html templates are stored
    template_directory = os.path.dirname( \
                            os.path.abspath(__file__)) + "/templates"

    #The cache file to use for movies
    movie_cache_file = "movieCache.p"


    def __init__(self):
        raise Exception("You shouldn't instantiate this class.")
