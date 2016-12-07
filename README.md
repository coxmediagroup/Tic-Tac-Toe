# Tic-tac-toe code challenge

This is a fork of a repository set up by a company as a hiring interview "code challenge." The goal: implement a tic-tac-toe (aka noughts and crosses) game, where the computer player couldn't be beaten.

My attempt was made way back in February 2011. Back then I knew some git, some Python, no Django, and very little about unit testing, but since the company I was applying to was a Django shop, I read the docs and built my Tic Tac Toe game as a Django app.

Even though I got the job, I knew the implementation could be smaller, faster, stronger, more efficient. Tic-Tac-Toe is a simple enough game that [an AI can run in a 1952 EDSAC][OXO], an implementation that makes it the [oldest graphical computer game][NC]. Six decades later, I shouldn't be satisfied with a giant Django-based implementation that takes several hundred milliseconds to run. I should be able to craft something super tiny and super fast.

My original Django-based work is in one of the branches in the git history. The files currently here a little spikes of ideas I've had to make the solution as small, elegant, fast, or efficient as I can, just as an exercise.

New challenge: *a computer player for a game of tic-tac-toe that computes the best next move for any given game state in constant O(1) time, using the smallest possible constant amount of memory.*

## Recent ideas

("Recent" for this repository means more than 2 years ago.)

1. Completely separate the UI from the game engine.
2. For speed, the board should be a [bitboard][], the functions that check for a win should use bitwise operations.
4. The game has 9 squares and thus an upper bound of 9! possible arrangements of pieces on the board, if examined naively (considering each piece to be unique; playing until the board is full despite early wins.) If we were to pre-compute and store the "best next move" for all possible gamestates as a byte, that's only 362k of memory, only 362k leaves in a game-tree to explore. (Then, the problem is reducable to mapping any given game-state to an enumeration of game-state permutations, to locate the position in our solutions array.)
    - The game will sometimes end before filling up all squares, so that reduces the total number of possibilities.
    - The optimal move is not affected by the order of moves, so some of those game-states are equivalent, reducing further the total number of possibilities.
    - The board has dihedral symmetry of order 8, so every game-state and its best-next-move may have up to 8 equivalent game-states under some combination of rotation and reflection. In fact, taking symmetry into aaccount, [there are only 765 possible game-states][mathrec02]. If we find a way to trivially determine a canonical symmetry for any given game-state (maybe the lowest value when the bitboard is cast to an integer?), we can greatly reduce the computation and storage requirement to map the entire game-space.
    - After determining a minimal set of game-states, a canonical way to represent them as integers, a way to rotate any given game-state into a canonical form and invert it afterward, and their mapping to next-best moves, if the set is small enough, we may be able to discover a polynomial function over the integers modulo 9 that generates the next-best move instead of our having to store it, maybe first searching for a modulus to apply to the input space to make the former task easier. Presto: a mathematical function for tic-tac-toe, given a canonical rotation of the board.

## License

I don't know why you would want to use any of this code, but if you do, you may do so under the terms of the [GNU Affero General Public License version 3][AGPL] or (at your option) any later version.

[AGPL]: http://www.gnu.org/licenses/agpl.html
[OXO]: https://en.wikipedia.org/wiki/OXO
[NC]: http://www.pong-story.com/1952.htm
[bitboard]: https://en.wikipedia.org/wiki/Bitboard
[mathrec02]: http://www.mathrec.org/old/2002jan/solutions.html
