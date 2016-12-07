# Tic-Tac-Toe

## ttt
ttt is a package that provides a Tic-Tac-Toe library.

### ttt.Board
Simple implementation of a game board.  Nothing tic-tac-toe specific in it, and could be reused in other game engines.

#### members

* squares - List of squares on the board.  The value is either None if the square is available, or the player's marker

#### methods

* is_full() - returns True if there are no available squares, otherwise False
* is_empty() - returns True if all squares are available, otherwise False
* square_free(square) - returns True if **square** is available, otherwise False.  Raises ttt.BoardException if **square** is not valid for the board
* place(square, marker) - puts **marker** value on **square** as long as the board is not full and **square** is an available space.  Raises ttt.BoardException if **square** is invalid
* clear(square) - makes **square** an available space on the board.  Raises ttt.BoardException if **square** is invalid

### ttt.AbstractGame
The meat of the package.  Implements the main game loop and calls out to the UI for display or input.  Not usable on it's own and needs to be implemented to handle UI

#### members

* winner - either None if came is still in play or the player object that has won the game.
* board - current board game, see ttt.Board

#### methods

* \__init__(player1, player2) - Create an instance of the game to play.  **player1** and **player2** should be either an instance of ttt.ComputerPlayer or the UI's version of ttt.AbstractPlayer.
* play() - starts the main game loop.  Returns when the game is over.
* display_board() - called when the UI process should paint the board for the user.  *NOTE*: is not called when the player is ttt.ComputerPlayer
* display_finale() - called when the UI process should paint the winner of the game.  *NOTE*: this is called right after display_board() is called, so this function should not worry about painting the finished board.

### ttt.AbstractPlayer

#### members

* marker - Symbol used to represent the player on the board.  Traditionally "X" or "O" but anything can be used

#### methods

* get_square(current_board, previous_move, message) - Called by the main game loop to get the current player's next move.  The UI process should ask the user for their choice square and return the integer representation of that square.  **message** will be non-empty if there is something wrong with the choice the player made and should be displayed to them before asking them to make a choice.  **current_board** is the current playing board and **previous_move** is either None if this is the first move or the last square played by the opponent.  Both are used by the NPC and probably should not be used, although **previous_move** could be used to highlight the information to the human player.

### ttt.ComputerPlayer
The unbeatable NPC.  Nothing to implement, just instantiate and pass as one or both players into UI version of ttt.AbstractGame

## Implementing a new UI
Creating a new front end to ttt is really easy.

1. Create a class that inherits from AbstractGame and overrides display_board() and display_finale().
2. Create a class that inherits from AbstractPlayer and overrides get_sqaure.
3. Instantiate an instance of your player class and an instance of ComputerPlayer()
4. Pass the two player objects into an instantiation of your game class
5. call your game object's play() function

The engine handles the rest

## Reference implementation
text_ttt.py shows how simple it is to build a Tic-Tac-Toe application off the ttt package.  You can play the application as:

1. NPC vs NPC - not very exciting, will always end in a draw
2. Human vs NPC - you can choose either X or O.  Hope you are good!
3. Human vs Human - alternate moves

### command line arguments

* -p [0|1|2]  - number of human players
* -m [X|O]    - marker to use in single human player game