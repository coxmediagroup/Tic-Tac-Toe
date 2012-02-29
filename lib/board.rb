#
#  class:         Board
#  extends:       --
#  module:        TicTacToe
#
#
#  description:
#
#   Encapsulates the matrix used to record the state of a tic-tac-toe game.
#
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  class Board

    attr_accessor :size, :matrix
    
    DEFAULT_SIZE = [3,3]

    #
    #  Board.new takes an optional :size parameter which indicates the size of the
    #  matrix to construct.
    #
    #  Alternatively, Board.new can take an optional :matrix parameter with the
    #  intended 'state' for the board to have.
    #
    #  Note that the board's elements are integer-valued, with 0 representing
    #  an empty space. Positive integer values indicate the player -- 1 will be
    #  taken to be the player to go first, 2 the second.
    #
    def initialize(opts={})
      @size    = opts[:size]   || DEFAULT_SIZE
      @matrix  = filled_matrix(0,size)

      if opts[:matrix]
        matrix = opts[:matrix]
        matrix.each_with_index do |row, x|
          row.each_with_index do |value, y|
            inscribe!(value, [x,y])
          end
        end
      end
    end

    #
    #  Output the current state of the board. Optionally accepts a mapping to
    #  instruct the printer how to translate the integer-valued board elements.
    #
    #
    def pretty(value_map=[' ','X','O'])
      txt = StringIO.new

      @matrix.each_with_index do |row, n|
        txt << row.map { |value| " #{value_map[value]} " }.join('|') << "\n"

        # draw a line between each row
        txt << "-"*((3*@size[0])+(@size[0]-1)) << "\n" unless n == @matrix.length-1
      end

      txt.rewind
      txt.read
    end



    #
    #
    #  A public facility for placing a move, with a sanity check for not
    #  marking the same cell twice.
    #
    #
    def inscribe!(mark, position)
      
      raise ArgumentError.new("second argument must be an array-valued position") if not position.is_a? Array

      x, y = position[0], position[1]

      # puts "--- attempting to inscribe board at row #{x}, column #{y} with mark '#{mark}'"
      if at(x,y) != 0
        raise ArgumentError.new("may not mark a board position ([#{x},#{y}]) already marked (as #{at(x,y)})")
      end

      @matrix[x][y] = mark
      
      nil      
    end



    #
    #  Dimension-indirection helper to provide direct access to values in
    #  the underlying board matrix.
    #
    def at(x,y)
      # p @matrix
      # puts "--- attempting to find value at row #{x}, column #{y}"
      value = @matrix[x][y]
      # puts "--- returning #{value}"
      value
    end




    #
    #  Iterator yielding the elements of the board matrix in order
    #  also yielding the position (as the first and second elements of an
    #  array.)
    #
    def each_with_position
      @matrix.each_with_index do |row, x|
        row.each_with_index do |cell, y|
          yield [cell, [x,y]]
        end
      end
    end

    
    #
    #   Collect positions which are open and so legal to play
    #
    def unmarked_positions
      unmarked = [] # each_unmarked_position
      each_with_position { |val, pos| unmarked << pos if val == 0 }
      # puts "--- found unmarked positions: "; p unmarked
      unmarked
    end

    #
    #  Utility to determine whether a win condition or draw has occurred.
    #
    #  There are a few ways this could be a bit more sophisticated. The most
    #  clear to me is that we could determining whether any possible future set
    #  of legal moves could produce a win condition for either side (if not it's
    #  basically already a draw.)
    #
    #
    def done?
      return true if board_filled

      # there's a win if every element in the line are the same (and not empty)
      each_row_column_and_diagonal do |line| 
        return true if line.uniq.size == 1 and not line.uniq == [0]
      end

      false
    end


    #
    #   Determine which player won the game; return that player's number.
    #
    #   Note there are some 'mutant' edge cases here I'm not even bothering to consider --
    #   that there are multiple winning lines/rows, etc. (These are not legal
    #   game states anyway.)
    #
    #   Throws a StandardError if the game isn't finished (isn't a draw/win/loss.)
    #
    def winner
      
      raise StandardError.new("winner cannot be determined at this stage in the game") if not done?

      each_row_column_and_diagonal do |line|
        return line.first if line.uniq.size == 1 and line.uniq != [0]
      end

      # since we complained if we've been invoked when the game couldn't be called yet,
      # the game appears to be a draw
      nil
    end
    


    private

    #
    #  Internal helper utility for assembling a mxn Array with a particular value.
    #
    def filled_matrix(mark, size=DEFAULT_SIZE)
      Array.new(size[0]) { Array.new(size[1]) { mark }}
    end

    #
    #  Internal helper to determine whether there are any empty spaces on the board
    #
    def board_filled
      @matrix.each do |row|
        row.each do |cell|
          return false if cell == 0
        end
      end
      true
    end # end private board_filled

    #
    #  Internal helper for gathering the diagonal elements. Assumes a square board.
    #
    def diagonals
      [ (0...@size[0]).collect { |i| @matrix[i][i]    },
        (0...@size[0]).collect { |i| @matrix[i][@size[0]-1-i] } ]
    end

    #
    #  Internal helper for iterating over both rows and columns.
    #  We can get these fairly directly by enumerating the board
    #  and its transposition.
    #
    def each_row_and_column
      (@matrix + @matrix.transpose).each { |line| yield line }
    end

    #
    #   Identical to each_row_and_column, but grabbing the diagonals as well.
    #
    def each_row_column_and_diagonal
      (@matrix + @matrix.transpose + diagonals).each { |line| yield line }
    end

  end # end Board
end # end TicTacToe