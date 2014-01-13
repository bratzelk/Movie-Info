printf "Movie Info Test Suite \n\n"

printf "Running Unit Tests...\n"
python ./tests/unitTests.py


printf "\nChecking Internet Connection...\n"
curl -D- -s http://www.google.com > /dev/null
if [[ $? == 0 ]]; then
    printf "Working!\n"
else
    printf "Connection Failed!\n"
    printf "Exiting Tests.\n"
    exit 1
fi

printf "\nChecking for movies...\n"
python ./src/main.py -d ./tests/testMovieDirectory -limit 500

printf "\nDone!\n"