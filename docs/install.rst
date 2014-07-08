cOXtactoe
=========

Pre-requisites
--------------
- Bash
- Git
- SQLite3


Installation & Configuration
----------------------------

0. Set installation/path options.

.. code-block:: bash

    $ INSTALL_DIR="$HOME/code"
    $ TTT_PROJ="tictac"

1.  Install virtualenv, pyenv, and pyenv-virtualenv

    * pyenv: `https://github.com/yyuu/pyenv`
    * pyenv-installer: `https://github.com/yyuu/pyenv-installer`
    * pyenv-virtualenv: `https://github.com/yyuu/pyenv-virtualenv`

NOTE
~~~~
If you already have Python 2.7.x and virtualenv, you may simply create a new
virtual env and skip the pyenv/pyenv-virtualenv setup. If you do skip the pyenv
installation make sure to use the appropriate virtualenv path in step #6.


Installation
~~~~~~~~~~~~
You may use Homebrew if you have it or alternatively, use the installer.


Homebrew
~~~~~~~~
.. code-block:: bash

    $ brew install pyenv pyenv-virtualenv


Manual Install
~~~~~~~~~~~~~~
.. code-block:: bash

    $ cd $INSTALL_DIR
    $ git clone https://github.com/yyuu/pyenv-installer.git
    $ bash ./pyenv-installer/bin/pyenv-installer
    $ echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
    $ echo 'eval "$(pyenv init -)"' >> ~/bashrc
    $ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    $ exec "$SHELL"


2.  Install Python-2.7 with pyenv


`OS X`

use Homebrew or MacPorts if the build process complains of a missing library.


`Ubuntu`

.. code-block:: bash

    $ sudo apt-get libreadine-dev libbz2-dev zlib1g-dev libsqlite3-dev libssl-dev


`On Both`

.. code-block:: bash

    $ pyenv install 2.7.7
    Installing Python-2.7.7...
    Installed Python-2.7.7 to /Users/username/.pyenv/versions/2.7.7
    $ pyenv rehash


3. Create and activate pyenv virtualenv

.. code-block:: bash

    $ pyenv virtualenv 2.7.7 $TTT_PROJ
    $ pyenv activate $TTT_PROJ


4.  Clone this repo where you keep your project source code

.. code-block:: bash

    $ cd $INSTALL_DIR
    $ git clone https://github.com/bzdzb/Tic-Tac-Toe.git $TTT_PROJ
    $ cd $TTT_PROJ


5.  Customize settings (optional)

    If you would like to update your TIME_ZONE or any other options, the
    settings files are located in `$TTT_PROJ/tictac/settings/`. They are
    organized into `base.py`, `dev.py`, `test.py`, `stage.py`, and `prod.py`.
    Only `base.py` and/or `dev.py` are likely to be of interest at this time.

    `Settings`

    * Base: `$TTT_PROJ/tictac/settings/base.py`
      Core configuration. Shared by other settings files.

    * Development: `$TTT_PROJ/tictac/settings/dev.py`
      Development specific settings. E.g. DEBUG=True, django_toolbar, etc.

    * Testing: `$TTT_PROJ/tictac/settings/test.py`
      Settings specific to running tests.

    * Stage: `$TTT_PROJ/tictac/settings/stage.py`
      Settings for stage deployment.

    * Production: `$TTT_PROJ/tictac/settings/prod.py`
      Settings for production deployment. E.g. DEBUG=False, production DB, etc.


6.  Add project to python library path.

.. code-block:: bash

    $ cd $INSTALL_DIR/$TTT_PROJ/tictac
    $ echo `pwd` > ~/.pyenv/versions/${TTT_PROJ}/lib/python2.7/site-packages/tictac.pth


7.  Set the `DJANGO_SETTINGS_MODULE` environment variable now, and on every
    virtualenv activation:

.. code-block:: bash

        $ export DJANGO_SETTINGS_MODULE=tictac.settings.dev
        $ echo "!!" >> ~/.pyenv/versions/${TTT_PROJ}/bin/activate
        $ exec "$SHELL"
        $ pyenv activate $TTT_PROJ


8.  Install the basic project requirements:

.. code-block:: bash

        $ pip install -r requirements/bin.txt
        $ pip install -r requirements/dev.txt

    As you edit your `requirements.txt` files, you can run those last commands again;
    `pip` will realise which packages you've added and will ignore those already installed.
