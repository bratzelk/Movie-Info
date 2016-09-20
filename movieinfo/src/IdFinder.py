"""This class will find an IMDB Movie id given a movie title
It can be used to help correct erroneous movie titles"""

import json
import re
import urllib
import logging
import time


class IdFinder(object):
    """This class will find an IMDB Movie id given a movie title
    It can be used to help correct erroneous movie titles"""

    _url_regex = r"imdb.com/title\/(.*?)\/"
    _lookup_domain = "imdb.com"

    def __init__(self):
        pass

    def _generate_lookup_url(self, title):
        """Generates the lookup URL for a given title"""

#search_url = "http://www.google.com/search?q=site%%3A%s+%s"% (domain, title)
        search_url = """http://ajax.googleapis.com/ajax/services/search/web?v=1.
                        0&q=site%%3A%s+%s""" % (self._lookup_domain, title)
        return search_url

    def find_id_by_title(self, title):
        """Find an IMDB ID using a movie's title"""

        #let's limit the number of requests to 0.5/second
        # to avoid sending too many requests
        time.sleep(2)

        logging.debug('Searching Google/IMDB for: %s', title)
        search_url = self._generate_lookup_url(title)
        results = json.load(urllib.urlopen(search_url))
        try:
            url = results['responseData']['results'][0]['url']
            imdb_id = re.search(self._url_regex, url).group(1)
            logging.debug('IMDB ID found: %s', imdb_id)
        except re.error:
            imdb_id = None
            logging.debug('IMDB ID not found!')
        else:
            imdb_id = None
            logging.debug('IMDB ID not found!')

        return imdb_id

    def find_id_by_title_list(self, title_list):
        """Find an IMDB IDs using a movie title list"""
        id_dict = {}
        for title in title_list:
            id_dict[title] = self.find_id_by_title(title)
        return id_dict
