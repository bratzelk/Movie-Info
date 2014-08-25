"""This creates a list of directories and filenames which match a regex
within a single directory it creates a list of matched filenames/directories
and list of ignored, or unmatched filenames/directories"""

import os 
import re
import logging


class Matcher(object):
    """This creates a list of directories and filenames which match a regex
    within a single directory it creates a list of matched filenames/directories
    and list of ignored, or unmatched filenames/directories"""

    #Stores a list of titles which were matched
    _match_list = []

    #A list of items which were ignored due to their file extension
    _ignored_list = []

    def __init__(self, match_regex, allowed_file_types):
        self._match_list = []
        self._ignored_list = []

        self._match_regex = match_regex

        self._allowed_file_types = allowed_file_types

    def _add_match(self, item):
        """Add a matched movie to the list."""
        self._match_list.append(item)

    def _ignore(self, item):
        """Add an ignored movie to the list."""
        self._ignored_list.append(item)

    def get_matches(self):
        """Returns the list of matched movies."""
        return self._match_list

    def get_ignored(self):
        """Returns the list of ignore movies."""
        return self._ignored_list


    @classmethod
    def _get_file_extension(cls, full_filename):
        """Extract file extension from the filename, if it exists."""
        try:
            (filename, extension) = full_filename.rsplit(".", 1)
        except:
            filename = full_filename
            extension = ""
        return (filename, extension)

    def _is_valid_extension(self, extension):
        """Check if a file extension is allowed."""

        #force all lowercase file extensions
        _allowed_file_types = map(lambda x:x.lower(), self._allowed_file_types)
        if len(extension) in range(1, 5) and extension.lower() \
                                    not in _allowed_file_types:
            return False
        else:
            return True

    def find_in_directory(self, directory):
        """Find items in a directory which match our rules."""

        #open the directory containing all of the matches.
        try: #could also use: os.path.isdir()
            os.chdir(directory)
        except:
            print "Error: Directory, %s does not exist!" % (directory)
            exit()

        #go through everything in the current folder
        for files in os.listdir("."):

            #Match our regex against everything in the folder
            matched = re.match(self._match_regex, files)

            #Add all items which matched the pattern to our list to lookup later
            if matched:

                item = matched.group()

                (item, extension) = self._get_file_extension(item)

                #if the file extension doesn't exist or is
                #allowed then we add the movie to the list
                if self._is_valid_extension(extension):
                    self._add_match(item)
                    #print item
                else:
                    #print "Ignoring Item: %s" % item
                    self._ignore(item+"."+extension)
