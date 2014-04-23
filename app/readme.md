
Running the Game
================

To run this project install the 'flask' module ("pip install flask" if you have pip, 
if you don't have pip you should be able to get it with "easy_install pip") 
then inside of the "app" folder run the "app.py" file on the command line. 

Go to http://localhost:5000 and have fun!

Notes
=====

To Develop this project I used:

* python 2.7.2
* flask 0.10.1

Flask and the flask dependencies are the only non-standard modules used.

Contact
=======

If you like it drop me a line!
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