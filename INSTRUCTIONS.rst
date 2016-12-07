Instuctions
===========

Unzip / Clone the repository into your working directory of choice.  All commands below
should be executed from within the working directory.

CLI
===

To run the CLI Interface, execute the following command:

python run-cli.py


Web Interface
=============

The web interface has a few pre-requisites.  Please install them by executing the following
command within your Python environment or virtualenv.

pip install -r requirements.txt

The web interface requires that the executing user has write access to the working
directory for creating sessions.  Additionally, the web interface starts a web server 
on port 5000; appropriate permissions and firewall exceptions may be required.

To start the web interface server, execute the following command:

python run-web.py 

Once the server is running, visit http://localhost:5000/ with your web browser.
