"""Some simple helper functions"""

class MovieDataUtil(object):
    """Some simple helper functions"""

    @staticmethod
    def sort_movie_data(movie_data):
        """sort our movie dictionary by their IMDB rating value."""
        movie_data = sorted(movie_data.iteritems(), reverse=True, \
                key=lambda (k, v): (v['imdbRating'], k))
        return movie_data

    @staticmethod
    def is_valid_lookup_result(movie_data):
        """Check if a movie lookup returned a valid response."""

        #probably not the best way to check this...
        if movie_data['Response'] == "True":
            return True
        return False
