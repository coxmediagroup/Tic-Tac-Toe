
# source this to activate virtual environment

echo Checking for virtualenv
virtualenv --version > /dev/null|| pip install virtualenv


mkdir -p var/bin
if [ ! -e var/bin/activate ]; then
    echo -n Creating virtual environment...
    virtualenv var > /dev/null
    echo done!
fi

echo Activating virtual environment...
. var/bin/activate

echo -n Installing any necessary libraries...
pip install -r requirements.txt > /dev/null
echo done!
