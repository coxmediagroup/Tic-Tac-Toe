#
# An abstract class with a basic contract -- inheriting classes
# should implement a method called 'next_move' which takes a TicTacToe::Board
# object as its single argument, and returns an array-valued position
# indicating the next move to be placed.
#
module TicTacToe
  class Player

    attr_accessor :number

    #
    #
    #
    def initialize(player_number)
      puts "--- creating new player with number #{player_number}"
      @number = player_number
    end

    #
    #  Mark the board with the player's next move, determined
    #  by invoking 'next_move'
    #
    def move(board)
      puts "=== It is player #@number's move."
      play = next_move(board)
      puts "--- Player has decided to move at #{play[0]}, #{play[1]}."
      board.inscribe! @number, play
    end

    # abstract def next_move; ...; return [x,y]; end

  end
end
