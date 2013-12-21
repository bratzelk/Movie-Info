#####################################################
#Movie Info 0.5
#By Kim Bratzel 2014
#####################################################


Movie Info currently loops through a folder of movies, it looks at all filenames and directory names within this folder and uses this information to looks up each movie using a 3rd party API. 
It then outputs every movie's title which it matched and returns them in order of their IMDB rating.

It can now also output a much more advanced web page with details on all of the matched movies. The web pages allows you to sort by any of the IMDB attributes and it includes an image of each movie's poster, so you can visualise your collection!

This is still very much a work in progress.


#####################################################
#Dependencies
#####################################################
#python
#jinja2 - http://jinja.pocoo.org/ - sudo pip install jinja2

#####################################################



#####################################################
#Usage Examples
#####################################################

#python movie.py -d ./tests/test01              -html -limit 500  > example-output.html
#python movie.py -d ./tests                           -l 900      > example-output.txt

#python movie.py -dir /Volumes/My_Book/Movies   -html             > example-output.html
#python movie.py -dir /Volumes/KIM/TV Shows     -html -limit 500  > example-output.html

#python movie.py -h (help)
#python movie.py -v (version)


#The most important part is the directory where your movies are stored
#They can be files or folders within that directory

#####################################################



#####################################################
#ToDo
#####################################################
#More Sanity/Error Checks
#Make HTML Pretty (Bootstrap etc)
#Add a list of movies which weren't found to the HTML output
#Improve the Movie Matching (ignore files which aren't movies)
#Start test cases and run script
#Much more...
#####################################################
