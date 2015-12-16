# Tracy's Tic Tac Toe Game

###Features

####UI
* The UI is responsive and has been tested using Chrome's device mode for several device formats.
* A maximum size of 600px has been chosen.

####Game Options
* The Game Options form will be visible by default on first opening.
* The options form can be opened and closed by clicking the link.
* The link text (+ / -) toggles accordingly.
* The options form closes automatically on any game play
* Selected options are persisted between browser refreshes.
* Options:
 * Mark: The user can select "X" (default) or "O". They are player One and their color is green. The AI plays second and its color is blue.
 * Competitors: The user cn select from four play modes:
  * Player vs Player: Two humans may play.
  * Player vs AI (default): A single player plays against the computer.
  * AI vs AI: The computer plays against itself. Click "New Game" to start play. The opening play will be the center or a corner and there will be five games played automatically.
  * TEST: The computer plays against itself but all possible starting moves will be tested so there will be nine games played automatically.
 * AI Level: On the "Smart" (default0 setting, the AI will never lose. On the "Dumb" setting, the AI plays randomly and can loose easily
 * AI Think Delay: A timeout simulates the AI thinking. On zero, there is no delay. default: 500
 * Auto New Game: Applies only when at least one human is playing. Starts a new game after end of previous game. AI only games always run automatically. default: 2000

####Scoreboard / Game buttons
* There is a row for each player, colored accordingly.
* The "Mark (Type)" column displays the selected mark, the tpe of player (human or AI) and indicates the AI level in effect.
* The "Wins!" column counts the wins for each player.
* The "Draw" column counts the number of tie or draw games.
* "Reset Game" clears the scoreboard, but "New Game" does not.

####Game Board & Play
* Play is would be expected.
* A play cannot be retracted.

####Notes
* The AI play algorithm is an original, manual implementation of basic rules outlined in the first commit.
* A valid "To Do" would be to replace the manual logic with an implementation of the "minimax" algorithm.
* jQuery is the only library utilized.


Story
======

As a CMG manager, I want to see how you code a game of Tic Tac Toe, so that I can get a feel for a candidate's skills and strengths.

Acceptance criteria
=======================
* Application is a stand alone, static web page game of tic tac toe.
* Computer (AI)  will never lose a game.
* Application should be able to run based on HTML, CSS and Javascript.
* Game will let player choose to be either X or O, computer will take other choice.
* Game will let player go first.

Submission Tips
========================
* Quality counts! A good submission that takes a while is better than a poor submission quickly. 
* Make sure your submission accurately reflects your development style.
* Commit early and often, with good messages.
* Comments and Unit tests are appreciated but not required, if you know good practice, then show us.
* Research the AI, there are multiple well known algorithms available, show us your implementation.
* Plagarism will not be tolerated.


Submissions
---------------
* Fork this repo and send us a pull request.
* if you prefer you can send us a ZIP of your submission, due to email filters, rename the file to *.txt and mention it is a ZIP in your email.

