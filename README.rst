Running
=======

To run this project, the Bower_ tool is required.

To run this project, after cloning:

1. Setup an environment with Python 3.3 (e.g. ``mkvirtualenv tictactoe -p python3``)

2. ``pip install -r requirements.txt``

3. ``python manage.py bower install``

4. ``python manage.py runserver``

After this, navigating a browser to ``http://localhost:8000`` should show an
empty board where you can begin to play.


Issues
======

I couldn't devise a good strategy to test the client independent of the
server, so the Javascript has only been manually tested. In normal
circumstances I would've spent more time searching for a solution or otherwise
sought help, but in the interests of finishing this project in a reasonable
timeframe I opted to skip testing. That said, there are still automated tests
of the server-side code.

Contact information
===================
I spoke to a recruiter who informed that you guys are looking for Django
developers, and that I should complete this project to apply. I assume he's
already contacted your group with my resume, but in case anything's missing,
feel free to contact me directly at danpassaro@gmail.com.

.. _Bower: http://bower.io/