@echo off

rem no need to pollute the main python installation
echo ***[configuring project virtual environment...]

pip install "virtualenvwrapper-win>=1.1.5"
pip install --upgrade virtualenv
call mkvirtualenv test-bryce-eggleton
call workon test-bryce-eggleton

echo ***[virtual environment configured.]
echo ***[installing required Python packages...]

pip install -r requirements.txt

echo ***[packages installed.]
pause
