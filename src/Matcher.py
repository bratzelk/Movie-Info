import os 
import re


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
