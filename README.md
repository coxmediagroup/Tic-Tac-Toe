## Tic Tac Toe

This Django project allows the user to play a game of Tic-Tac-Toe with a reasonably skilled AI opponenent.  It's not perfect, but it is realistic.  I simply ran out of time to debug the rest of the MinMax algorithm.

#### Pre-Requisites

- Virtualenv (http://www.virtualenv.org/en/latest/)
- SQLite 3 (http://sqlite.org/)

#### Getting started

- Check out a copy of this repository.
- Inside of this directory run `virtualenv venv` to create the virtual environment.
- Run `source venv/bin/activate` to activate the virtual environment.
- Run `pip install -r requirements.txt` to install the rest of the dependencies.

#### Running the tests

There is a (very) small suite of tests.  They can be ran by running: `python manage.py test`

#### Syncing the database

While not necessary, this app logs all moves and board positions.  There isn't any real functionality that uses this, but it does show that I know how to wire up models, the admin, and use standard database concepts.

- Run `python manage.py syncdb`
- Run `python manage.py migrate`

As is best practice, South was used to handle schema migrations.

#### Running the server.

To get running, just do the usual: `python manage.py runserver`.

### General Notes

As I was going through the process of creating this, I had a few thoughts as to what I would do differently if I had more time.

- Perfecting the AI.  Yes, the AI is flawed.  I wasn't able to make it perfect, but it is actually more fun to play against this was in my opinion.
- Better win detection.  There are still some instances where a win has occurred by the AI, but it never registers.  I'm flummoxed.
- More, better tests.  The testing is fairly high level integration testing.  I'd like some unit tests around the TicTacToe class.
- Use an API framework.  Ideally I'd use Django Rest Framework, but TastyPie would be fine too.  Having nice client-server seperation and a good REST interface to communicate with is nice.
- Use Angular.js.  I have expert knowledge of Angular, but I didn't think this would be as complicated as it became on the frontend.  I would definitely use a client-side framework next time instead of just jQuery.
- It would be great to save games and start back from that position.
- It could use some design love, but at least Bootstrap3 provides something.
- I should use Django-Compressor to compress my CSS and javascript.
- I really should be using SASS or LESS for CSS.  Once again, the scope grew further than I was expecting.
- I would have liked to deploy this somewhere, but I think that was beyond scope.