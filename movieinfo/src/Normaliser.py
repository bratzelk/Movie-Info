import logging

class Normaliser(object):
    """Helper functions for normalising and manipulating strings"""

    def __init__(self):
        pass

    @staticmethod
    def remove_trailing_number(string):
        """NOTE: This whole method needs rethinking... will probably remove
        it completely and ignore strings in the pattern match...If the last
        four to six chars of a string are a number (with or without braces),
        remove them. This might cause a problem with some movies..."""
        
        braces = ["{", "}", "(", ")", "[", "]"]

        #first check if there are braces and a number at the end of the string
        #if so remove them
        if string[-1] in braces and string[-6] in braces and \
        string[-5:-1].isdigit():
            return string[:-6]

        #now check if there is just a number at the end...
        last4chars = string[-4:]
        if last4chars.isdigit():
            #remove the string
            return string[:-4]
        else:
            #keep the whole string
            return string

    @staticmethod
    def normalise(string):
        """Normalise a string"""
        return string.lower().strip()

    @staticmethod
    def normalise_list(list_of_strings):
        """Normalise a list of strings"""
        new_list = []
        for item in list_of_strings:
            new_list.append(Normaliser.normalise(item))
        return new_list

