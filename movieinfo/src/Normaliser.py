import logging

class Normaliser(object):
    def __init__(self):
        pass

    #NOTE: This whole method needs rethinking... will probably remove it completely and ignore strings in the pattern match...
    #If the last four to six chars of a string are a number (with or without braces), remove them
    #This might cause a problem with some movies...
    def removeTrailingNumber(self, string):
        braces = ["{","}","(",")","[","]"]

        #first check if there are braces and a number at the end of the string
        #if so remove them
        if string[-1] in braces and string[-6] in braces and string[-5:-1].isdigit():
            return string[:-6]

        #now check if there is just a number at the end...
        last4chars = string[-4:]
        if last4chars.isdigit():
            #remove the string
            return string[:-4]
        else:
            #keep the whole string
            return string

    def normalise(self, string):
        return string.lower().strip()

    def normaliseList(self, list):
        newList = []
        for item in list:
            newList.append(self.normalise(item))
        return newList