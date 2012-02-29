#
#  class:         ComputerPlayer
#  extends:       Player
#  module:        TicTacToe
#
#  description:
#
#   Provides an optimal TicTacToe opponent, utilizing a minimax algorithm to
#   determine the best move. We construct the tree of legal interactions between
#   players beginning from our current position, assigning scores to endgames
#   based on their disposition. These scores propagate up the tree and
#   acculumate; we pick the best-performing branch.
#
#   The method here could be more sophisticated in a number of ways; for instance
#   we could do more aggressive caching of the results of analysis to optimize
#   future searching. (Indeed the game is small enough that a table of all
#   possible legal boards and the corresponding optimal play is trivial to
#   construct and small in size.)
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
    #  Determine the next play by identifying the highest-scoring legal move
    #
    def next_move(board)
      board.unmarked_positions.max_by { |pos| score_move(board, pos) }
    end

    #
    #  Assign a score based on the disposition of the board
    #
    def score(board)
      raise ArgumentError.new("cannot determine disposition while game incomplete") unless board.done?

      if board.winner == nil
          0 # draw
        elsif board.winner == @number
          1 # win!
        else
          -1 # loss...
        end
    end

    #
    #
    #    Analyze hypothetical move through exhaustive construction of
    #    possible future play, minimizing the chance of losing.
    #
    #
    def score_move(board, position, my_move=true)
      unless board.done?
        
        # mark a new board to pass to subroutine
        updated_board = Board.new(:matrix => board.matrix)
        updated_board.inscribe!(  @number, position)     if my_move
        updated_board.inscribe!(3-@number, position) if not my_move

        # check if we're done already
        unless updated_board.done?
          updated_board.unmarked_positions.inject(0) do |score, next_position|
            score + score_move(updated_board, next_position, !my_move)
          end
        else
          score(updated_board)
        end
      else  # score it
        score(board)
      end
    end

  end
end
