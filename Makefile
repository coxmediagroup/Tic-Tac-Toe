all: run

install: virtualenv javascript

virtualenv:
	if [ ! -d ve ] ; then virtualenv ve ; fi
	ve/bin/pip install -r requirements.txt
	ve/bin/python setup.py develop

run:
	ve/bin/python manage.py runserver

javascript:
	npm install
	bower install
