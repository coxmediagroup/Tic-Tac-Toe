readme.txt

tictactoe app in python that can interactively play the game and never lose.

Acceptance criteria
The AI should never lose
Server is the Python cgi-server and server code in tictactoe,py
Client is the POST CGI HTML Form in tictactoe.,py
Decided to integrate into one, although the function was tested standalone CLI before
integrating it into the 'web app' as a whole
Another server piece is a file created by the app that persists the state of the tictactoe board during play
Strengths include ability to have small footrprint, ease of use, copious and wide range of testing (including corner cases not just main flow)
Testing includes measuring high throughput performance, large number of trials, testing not only code but instructions to configure 
Did a lot of initial work/research before the git workflow so yes, submission took awhile
Clear instructions for how to run your application


Pre-requisites:
 Windows, Mac, Linux
 Python 2.7+ interpretor
 Web browser

 readme.txt
 cgi-bin/tictactoe.py 
 # make sure first line in code points to your python interpreter



1. 
tar xvf 
You should end up with:
readme.txt
cgi-server/
	tictactoe.py

2. Peruse commit history, etc

3. Run Python cgi-server 
   python -m CGIHTTPServer
   This ensures we are client-server, not just CLI only nor browser only but BOTH

4. Point Web Browser to 
    http://localhost:8000/cgi-bin/tictactoe.py





Style notes
 Although there were a lot of examples on the web , I decided to start from basic principles
 My development style features copious testing, small footprint, ease of use, transparency of design,
 where testing includes functionality, performance, compatibility, and instructions
 Also I minimize dependencies, in this case, python and web browser are all you need
 
Submissions
Publicly: Fork this repo and send us a pull request.
Privately: Send us a tar.gz of your solution including your .git folder so we can see your commit history.
