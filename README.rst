Noughts and Crosses
===================

Foreward
--------

Firstly, let me thank you for taking the time to consider me as a candidate for 
employment. While not strictly necessary to achieve the goal of the project, I chose
to use Django since I am familiar with and have experience working with it.

There are further instructions below on how to quickly launch this project within an 
instance of the Django dev server. If you are running Windows, there are also batch 
files which can be run to take care of installing required python packages as well 
as running a local dev server.


Requirements
------------

Python 2.7.5 and pip >= 1.4.1 are the only things that must be installed
in advance for this project to run on a Django dev server locally. Given 
the circumstances I imagine you already have those taken care of.

For Windows, your /Python27 as well as /Python27/Scripts directories
**must** be included in the system path environment variable, otherwise the 
setup batch file will fail.


Resume
------

You are welcome to contact me through LinkedIn, GitHub, or other avenues. 
I try to keep my LinkedIn account the most current, however, so that would be 
the best place to find up to date information.

`My LinkedIn Profile <//www.linkedin.com/pub/bryce-eggleton/84/850/713>`_


Quickstart
==========

Windows
-------

1) run setup.cmd (django setup can take a couple minutes just give it a litte time)
2) run launchdev.cmd
3) navigate to 127.0.0.1:8000 in a browser
4) play noughts and crosses
5) close dev server
6) run uninstall.cmd


Linux
-----

Unfortunately I don't have any Linux installations right now, or I would have included 
bash scripts as well, so instead, below are the shell commands which should allow a 
fairly painless setup and launch. It is assumed that you are in the main project 
directory for these commands.

Create a virtual environment:
	``pip install virtualenvwrapper``
	``pip install --upgrade virtualenv``
	``mkvirtualenv test-bryce-eggleton``
	``workon test-bryce-eggleton``

Launch the dev server:
	``workon test-bryce-eggleton``
	``python manage.py runserver --settings=core.config``

Remove Virtual Environment:
	``deactivate``
	``rmvirtualenv test-bryce-eggleton``


Shell Script Files
==================

setup.cmd
---------

This file will create a virtual environment for the Python packages this 
project requires so as not to pollute your main Python installation. 
Then it will install any required Python packages for the project, including 
Django into the virtual environment. At that point, the project should be 
completely configured and ready to run, via the next script.


runserver.cmd
-------------

This will launch an instance of the Django dev server with the project 
settings and at that point, an interactive game of Noughts and Crosses 
will be available from your browser at 127.0.0.1:8000


uninstall.cmd
-------------

This file simply removes the virtual environment created from the setup.cmd 
script to leave almost no trace of the project.


TODO
====

#) darken out board a bit once the game is over
#) make the game status text more prominent
#) highlight what each player's last move was

