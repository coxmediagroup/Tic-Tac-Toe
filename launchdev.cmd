@echo off

rem launch the dev server from manage.py

call workon test-bryce-eggleton
set PYTHON_SETTINGS_MODULE=core.config
python manage.py runserver

rem in case there are any errors
pause


