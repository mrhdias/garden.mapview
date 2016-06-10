Easy way to test this example:

mkdir -p test/libs/garden
cd test/libs/garden
git clone http://github.com/mrhdias/garden.mapview.git
cp -r garden.mapview/examples/map_browser/* ../..
cd ../..
python main.py
