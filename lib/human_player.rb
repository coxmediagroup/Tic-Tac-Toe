#
#  class:         HumanPlayer
#  extends:       Player
#  module:        TicTacToe
#
#  description:
#
#   Provides a console-based interface for a human player to interact with
#   the TicTacToe game engine.
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  class HumanPlayer < Player

    def initialize(player_number)
      
      super(player_number)

      # gather the player's name
      puts "--- Let's play a game."
      puts "--- First, why don't you tell me your name?"
      @name = gets.chomp!

    end

    #
    #   Gather the player's next move entered as a two-digit
    #   number indicating the column and row the user wishes
    #   to mark.
    #
    def next_move(board)
      
      puts "--- It's your turn, #@name!"


      puts "--- Here's the current state of the board."

      puts board.pretty

      puts "--- We'll interpret your input as the row and column you wish to mark."
      puts "    (So, to mark the second row and third row, you'd enter '23'.)"

      # read from the console, validating the structure and content of the input
      valid_move_entered = false
      row, column = 0, 0
      until valid_move_entered
        puts "--- Please enter your next play (e.g., '12'): "
        next_play = gets

        # ensure it's the right length and only numbers
        if next_play.match(/[1-3][1-3]/)
          
          # validate the row and column are unmarked and within the board
          row, column = next_play[0].chr.to_i - 1, next_play[1].chr.to_i - 1
          # puts "--- Checking row #{row} and column #{column} for validity and presence of existing marks..."
          if board.get(row,column) == 0 and
             row >= 0 and column >= 0 and
             row <= 3 and column <= 3

             # alright! we should have a good position
             valid_move_entered = true
          end
        else
          puts "--- I will interpret your input as the column and row you wish to mark, entered without spaces or commas."
        end
      end

      puts "--- returning [#{row}, #{column}] as indicated position"
      [row, column]

    end

  end
end
