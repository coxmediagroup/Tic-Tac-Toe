
Background
==============

Web-based tic tac toe game for Cox Media Group.

The app uses:

::
    Python
    django 1.6

    backbone
    underscore
    jquery
    twitter bootstrap 3


and the front-end has been tested in:

::
    Chrome Mac 34.0.1847.116
    Safari Mac 7.0.3 (9537.75.14)
    Firefox Mac 27.0
    IE 11 Windows 11.0.9600.16384

and the backend on MacOS 10.9.2 and Amazon Linux AMI 2014.03

Installation
=================

To build:

* Check out code from github
* cd to root of checked-out code

::
    make


If you don't have Make, the following commands will build the code, assuming
python 2.7 is installed:

::
    . ./env.sh
    ttt/manage.py collectstatic --noinput
    ttt/manage.py syncdb --noinput
    ttt/manage.py migrate


To run in development:

::
    make develop

If you don't have Make installed, start the server with:

::
    . ./env.sh
    ttt/manage.py runserver 127.0.0.1:9999



To play, open the browser to http://localhost:9999/


To rebuild or clean:

::
    make clean

(or, non-Make folks):

::
    rm -Rf var
    rm ttt/db.sqlite3


MacOS X
-------------

* You'll need the XCode and cli stuff or gnu make installed.

