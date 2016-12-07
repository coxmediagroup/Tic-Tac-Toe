Tic Tac Toe You Can Never Win
=============================

This is a simple tic tac toe implementation build for deployment on Google App Engine. If I built it correctly, you should never be able to win. You can tie or lose at https://tic-tac-toe-you-can-never-win.appspot.com/.


Running locally
---------------

1. Clone this repository
2. Download and install the Google App Engine Python SDK
3. From the application directory, run ``<path_to_app_engine_sdk>/dev_appserver.py .``
4. Visit http://localhost:8080/


Running the tests
-----------------

1. Install the test dependencies: ``pip install webtest`` and ``pip install mock``
2. From the ``server`` directory, run ``python runtests <path_to_app_engine_sdk>``


Technical notes
---------------

* A Google account is required (it uses OAuth to create per-user games)
* The back end consists of a data model and a REST API built using Google Cloud Endpoints
* The front end uses AngularJS and the Google JavaScript Client Library
