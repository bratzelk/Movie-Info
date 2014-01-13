Movie Info 0.5
==============
By Kim Bratzel 2014
--------------

Movie Info currently loops through a folder of movies, it looks at all filenames and directory names within this folder and uses this information to looks up each movie using a 3rd party API. 
It then outputs every movie's title which it matched and returns them in order of their IMDB rating.

It can now also output a much more advanced web page with details on all of the matched movies. The web pages allows you to sort by any of the IMDB attributes and it includes an image of each movie's poster, so you can visualise your collection!

This is still very much a work in progress.




Dependencies
--------------

python 2.7+
jinja2 - http://jinja.pocoo.org/ - sudo pip install jinja2


Usage Examples
--------------

    python ./src/main.py -d ./tests/testMovieDirectory     -html -limit 500    > example-output.html
    python ./src/main.py -d ./tests/testMovieDirectory     -l 900              > example-output.txt

    python ./src/main.py -dir /Volumes/My_Book/Movies      -html               > example-output.html
    python ./src/main.py -dir /Volumes/KIM/TV Shows        -html -limit 500    > example-output.html

    python ./src/main.py -h (help)
    python ./src/main.py -v (version)

The most important part is the directory where your movies are stored
They can be files or folders within that directory



Tests
--------------

To run the tests (these aren't completed yet...)

    ./run_tests.sh
    


ToDo
--------------

 - Make HTML Pretty (Bootstrap etc)
 - Add some proper tests
 - Use an alternative API for failed lookups
 - Much more...


Contact
--------------

Get in touch: kimbratzel.com