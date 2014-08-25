import os
import logging

class Config:
    """This is where the application settings are found. """


    #####################################################
    #Some Basic Settings
    #####################################################

    #Logger Settings
    logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG, format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')

    #the amount of time to wait before timing out during each lookup
    timeout = 20

    #a list of filetypes to match (it will also match directory names)
    allowedFiletypes = ["tmp","avi","mpg","mpeg","mkv","mp4","divx"]

    #The regex pattern used to match movie names
    movieMatchRegex = "^[^.].+$"

    #The directory where the html templates are stored
    templateDirectory = os.path.dirname(os.path.abspath(__file__)) + "/templates"


    def __init__(self):
        pass;
