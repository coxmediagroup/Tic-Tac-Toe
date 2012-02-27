.. _DEPLOYNOTES:

DEPLOYNOTES
===========

Instructions for installation & upgrade notes.

Installation
------------

Software Dependencies
~~~~~~~~~~~~~~~~~~~~~

I recommend the use of `pip <http://pip.openplans.org/>`_ and `virtualenv
<http://virtualenv.openplans.org/>`_ for environment and dependency
management in this and other Python projects. If you don't have them
installed I recommend ``sudo easy_install pip`` and then ``sudo pip install
virtualenv``.


Configure the environment
^^^^^^^^^^^^^^^^^^^^^^^^^

When first installing this project, you'll need to create a virtual environment
for it. The environment is just a directory. You can store it anywhere you like;
in this documentation it will live right next to the source. For instance, if the
source is in /home/Tic-Tac-Toe, consider creating an environment in
/home/Tic-Tac-Toe/env. To create such an environment, su into apache's user
and::

  $ virtualenv --no-site-packages /home/Tic-Tac-Toe/env

This creates a new virtual environment in that directory. Source the activation
file to invoke the virtual environment (requires that you use the bash shell)::

  $ . /home/Tic-Tac-Toe/env/bin/activate

Once the environment has been activated inside a shell, Python programs
spawned from that shell will read their environment only from this
directory, not from the system-wide site packages. Installations will
correspondingly be installed into this environment.

.. Note::
  Installation instructions and upgrade notes below assume that
  you are already in an activated shell.

Install python dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tic Tac Toe depends on several python libraries. The installation is mostly
automated, and will print status messages as packages are installed. If there
are any errors, pip should announce them very loudly.

To install python dependencies, cd into the repository checkout and::

  $ pip install -r pip-install-req.txt

If you are a developer or are installing to a continuous integration server
where you plan to run unit tests, code coverage reports, or build sphinx
documentation, you probably will also want to::

  $ pip install -r pip-dev-req.txt

After this step, your virtual environment should contain all of the
dependencies for Tic Tac Toe.

Install the Application
~~~~~~~~~~~~~~~~~~~~~~~

Apache
^^^^^^

After installing dependencies, copy and edit the wsgi and apache configuration files
in apache inside the source code checkout. Both will probably require some tweaking for paths
and such.

Configuration
^^^^^^^^^^^^^

You will need to copy localsettings.py.dist to localsettings.py. Once done, go through
localsettings.py and enter in the appropriate data for your setup.

If running it in a development environment, then one will need to do the following
from the tictactoe directory of your checkout:

<pre>
    python manage.py syncdb
    python manage.py runserver
</pre>


Known Issues
""""""""""""

* Error checking is still very light. Beyond not handling many normal cases well (ie. DB down),
  some concerns to note: Incorrect form data isn't handled gracefully. Attempting
  to spam multiple invalid moves for the same exact game aren't really stopped as it is currently
  only prevented on the UI/Client level rather than on the server.

* Unit tests need to be fleshed out and have only partial code coverage.

* I used the deprecated "<center>" tag in two locations as I haven't had time
  to fully setup the design.