Movie Info 0.7
==============
By Kim Bratzel 2014
--------------

This program goes through your movie collection (folders or files within a directory) and uses movie titles to gather extra information about each movie using a third party API.

It generates a nice looking webpage which includes a sortable table containing each movie's cover image, title, IMDB Rating, and other data. It also creates coverflow style view of your movie collection ordered by IMDB Rating. User can also search for a specific movie by its title, IMDB Rating, Year, or any other information displayed on the table.

This is still very much a work in progress and in need of a lot of contributions.


Motivation and History
--------------

There are two motivations which drove the initial development of this project. Firstly I had access to too many movies which were of very varying quality. I needed a way of quickly sorting them in some kind of meaningful way to avoid watching the terrible ones first. I decided that sorting them by their IMDB rating would be the most efficient way to achieve this. Secondly I thought it would be a fun, bite-sized project to make open-source and allow others to contribute to.

Initially I wrote the whole script in a few hours in one relatively simple and yet long file. After I got it working I thought it would be nice to improve it, move to an OOP paradigm and share it with others. It still requires a lot of improvement and would be perfect for someone starting out their "open-source career" to get involved with. 


Installation (On Linux)
--------------

If you plan to install the package, you can do so by running this command at the root directory:

    sudo python setup.py install


Running The Program
--------------

Once you have installed the package you can run the program using:

    movieinfo -d movie_dir

Where `movie_dir` is the file or directory where you store your movies

Alternatively you can just run the program at the root directory using python directly if you don't want to install the package:

    python .movieinfo/src/main.py

See the usage examples below to understand how to run the program correctly.

Usage Examples
--------------

If you haven't installed the package replace "movieinfo" with "python ./src/main.py"

    movieinfo -h (help)
    movieinfo -v (version)

    movieinfo -d ./tests/testMovieDirectory     -html -limit 500    > example-output.html
    movieinfo -d ./tests/testMovieDirectory     -l 900              > example-output.txt

    movieinfo -dir /Volumes/My_Book/Movies      -html               > example-output.html
    movieinfo -dir /Volumes/KIM/TV Shows        -html -limit 500    > example-output.html


The most important part is the directory where your movies are stored. They can be files or folders within that directory.

"> example-output.html" will save all of the output of the program to a file named "example-output.html" in the current directory. You can then open this file to view the generated content.


Example Output
--------------

You can also generate some example HTML output by running the following script in `/movieinfo/scripts`:

    ./generate_example_html.sh

Tests
--------------

To run the tests (these aren't finished) run this script in `/movieinfo/scripts`:

    ./run_tests.sh

Change Log
--------------
 - 0.7
    - Local Caching
    - Various Improvements
 - 0.6
    - Erroneous Title Correction
    - CoverFlow View
    - Added Some Unit Tests
 - 0.5 Stable Release
 - 0.4 Beta


Dependencies
--------------

 - python 2.7+
 - [jinja2](http://jinja.pocoo.org) (sudo pip install jinja2)

ToDo
--------------

 - Make HTML Pretty
 - Cleanup the code
 - Finish writing the unit tests
 - Cache Lookups Locally (maybe using a pickle?)
 - Write the Wiki
 - Recommend Movies (Machine Learning)
 - Integrate some other APIs?
 - And more...


Contributing
--------------

I would love it if you would contribute to this small project!
Please read the [contributing](https://github.com/bratzelk/movie-info/blob/master/CONTRIBUTING.md) guidelines and get started.

Contact
--------------

Get in touch: [kimbratzel.com](http://www.kimbratzel.com)
