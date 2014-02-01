printf "Generating Example HTML Output... \n\n"

python ./src/main.py -d ./tests/testMovieDirectory     -html -limit 500    > example-output.html

printf "..Done. \n\n"
printf "You can now open example-output.html \n\n"