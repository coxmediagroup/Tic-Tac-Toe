
Running the Game
================

To run this project install the 'flask' module:

    pip install flask
    
If you don't have pip you should be able to get it with:

    easy_install pip
    
Then inside of the "app" folder run the "app.py" file on the command line. 

    python2.7 app.py
    

Go to http://localhost:5000 and have fun!

Notes
=====

To Develop this project I used:

* python 2.7.2
* flask 0.10.1

Flask and the flask dependencies are the only non-standard modules used. 
Optionally you can also run "server.py" which is the production version.
This uses the tornado library to serve the application. You will need to 
"pip install tornado" for this. I.E. seems hang on the built-in debug server,
this is a known bug in one of the dependency libraries.

Contact
=======

If you like the project drop me a line!
Aaron Decker, me@a-r-d.me


Test Notes:
==========

Visit http://localhost:5000/testai to test the ai. 
You should get something like this:

    {
      "cp_wins": 9591, 
      "ties": 409,
      "total_runs": 10000, 
      "user_wins": 0
    }
    
With the computer going first it should always win.


Browser Testing:
=================

* Chrome Latest: Working
* Firefox Latest: Working
* I.E. 11: Working if you run from server.py

