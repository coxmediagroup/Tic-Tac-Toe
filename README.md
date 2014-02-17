# Tic-Tac-Toe

## Original Intructions from coxmediagroup/Tic-Tac-Toe:

1. Fork this repo on GitHub
2. Create a program that can interactively play the game of Tic-Tac-Toe against a human player and never lose.
3. Commit early and often, with good messages.
4. Push your code back to GitHub and send us a pull request.

If you don't want to broadcast your intentions by forking this, feel free to
clone it and work locally. Then, send us a tar.gz of your solution, including
your .git folder so we can see your commit history.

We are a Django shop, but it is not a requirement that you implement your
program as a Django app.

## Installation

This application is packaged for Mac OS X, and you can simply drag
`tictactoe.app` from the `dist` folder into the desired location where you
would like to run it from.

The project was tested against 10.9 (Mavericks), and should be able to run on
10.6 or above. Please report any issues with these supported versions of Mac.

## Development

This project was built using [Kivy](http://kivy.org/), an open source library
for creating cross-platform apps using Python. You will need to follow the
instructions on their website for installation and setup if you would like to
run the project using the source files or to create an executable for your
particular platform.

In addition to installing Kivy, you should also install everything in
requirements.txt:

    pip install -r requirements.txt

The necessary project files can be found in the `app` folder. Tests are in the
`tests` directory and can be run using nose:

    nosetests
