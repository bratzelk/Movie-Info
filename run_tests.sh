echo "Running Test 01"
python ./tests/test01.py


echo "Checking Internet Connection..."
curl -D- -s http://www.google.com > /dev/null
if [[ $? == 0 ]]; then
    echo "Working!"
else
    echo "Connection Failed!"
    echo "Exiting Tests."
    exit 1
fi

echo "Checking for movies..."
python movie.py -d ./tests/test01 -limit 500

echo "Done!"