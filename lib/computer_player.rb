#
#  class:         ComputerPlayer
#  extends:       Player
#  module:        TicTacToe
#
#  description:
#
#   Should provide an computer tic-tac-toe opponent. Note this is turn an
#   abstract class so that we can work with different algorithms.
#
#   The contract is for subclasses to implement a 'rank' method by which
#   board positions of the same depth may be compared.
#
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#

module TicTacToe
  class ComputerPlayer < Player

    def initialize(player_id)
      super(player_id)
    end

    #
    #
    #  Determine the next play by identifying the highest-scoring legal move
    #  as determined by the 'rank' method (to be implemented in a subclass)
    #
    #
    def next_move(board)
      potential_moves = board.unmarked_positions
      puts "--- Evaluating #{potential_moves.size} possible moves."
      board.unmarked_positions.max_by do |potential_move|

        puts "--- Considering #{potential_move}"
        succ = Board.new :field => board.field
        succ.inscribe!(potential_move)
        
        score = rank(succ)
        succ.erase!(potential_move)
        puts "-- Got score #{score}"
        score

      end
    end
  end
end