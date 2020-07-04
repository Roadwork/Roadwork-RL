$EXECUTION_FOLDER=$(pwd).Path
$FILE_LOC=$PSScriptRoot + "/../../Lib/python/roadwork"
cd $FILE_LOC

echo "Creating Package..."
python setup.py sdist
pip install twine

echo "Uploading Package"
twine upload dist/*

# Back to execution folder
cd $EXECUTION_FOLDER