echo "Running Test 01"
python ./tests/test01.py

echo "Checking for movies..."
python movie.py -d ./tests/test01 -limit 500

echo "Done!"