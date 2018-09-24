rm -rf build
python setup.py install 
rm cyclus.sqlite
cyclus tests/try.xml