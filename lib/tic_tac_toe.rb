=begin

--- How do you win tic-tac-toe?

  Playing an optimal game of tic-tac-toe is effectively a minimax problem --
  the perfect move is one which maximizes one's chance of winning AND 
  which minimizes one's chance of losing.

  A standard method here would construct a tree of possible moves and countermoves,
  returning a score of +1,0,-1 indicating the disposition of the resulting endgame at the
  leaves of the tree. (We should be able to readily identify optimal moves.)

  Now, the most straightforward implementation I can imagine involves developing
  a complete tree for the game ahead of time (it's not very big). For the time
  being we'll regenerate the tree on each move.

  Finding myself curious about a few potential 'extensions' of the game,
  generalizations to a larger board and more players and so on, I'll try to build the
  core logic in a sufficiently abstract way to permit certain deviations from
  a standard game.

=end

require 'stringio'

require 'game'
require 'board'
require 'player'
require 'human_player'
require 'computer_player'

module TicTacToe

    VERSION = '0.0.1'
    AUTHOR  = 'Joseph Weissman <jweissman1986@gmail.com>'

    def self.banner; "TicTacToe v#{VERSION}. Written by #{AUTHOR}, 2012."; end

end