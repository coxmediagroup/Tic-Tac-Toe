#
#  class:         ComputerPlayer
#  extends:       Player
#  module:        TicTacToe
#
#  description:
#
#   Should provide an optimal tic-tac-toe opponent.
#
#
#   Wishlist:
#     - TODO get working! jeez.
#     - speed up with alpha/beta pruning
#     - use iterative deepening to provide configurable difficulty level
#     - could cache known results (perhaps wrap cache lookup in a method that knows
#       how to transpose/rotate the board matrices)
#
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#

module TicTacToe
  class MaximizingPlayer < ComputerPlayer

    def initialize(player_id=1)
      super(player_id)
    end

    def rank(board, depth=0)
      if board.done?
        score = evaluate(board) 
        return score
      end

      my_turn = board.turn == @number

      scores = []
      board.legal_next_states.each do |state|
        scores << rank(state,depth-1)
      end

      score = 0
      if board.turn == @number
        score = -scores.max
      else
        score = scores.min
      end
      score
    end

    def evaluate(board)
      if board.winner == 0
        result = 0
      else
        result = board.winner == @number ? 1 : -1
      end
      result
    end
 end
end
