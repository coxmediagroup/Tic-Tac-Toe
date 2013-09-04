============
SIMPLE-GAMES
============

A used a great template for django 1.5 from the book django-twoscoops.
You can find this template at [twoscoops](https://github.com/twoscoops/django-twoscoops-project/zipball/master)

Creating your project
=====================

To create a new Django project called '**simple-games**' using
django-twoscoops-project, run the following command::

    $ django-admin.py startproject --template=https://github.com/twoscoops/django-twoscoops-project/archive/master.zip --extension=py,rst,html simple-games

Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*

Run the app::
    $ cd simple-games
    $ python manage.py runserver