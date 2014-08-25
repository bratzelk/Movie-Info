#!/bin/sh

printf "Running the output generator...\n\n"


printf "Generating Stylesheets... \n"
./scripts/generate_stylesheets.sh
printf "..Done. \n\n"

printf "Generating Example HTML Output... \n"
python ./src/main.py -d ./tests/testMovieDirectory     -html -limit 500    > example-output.html
printf "..Done. \n\n"

printf "You can now open example-output.html \n\n"