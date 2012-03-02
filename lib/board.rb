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

    attr_accessor :field, :turn

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
      @field   = opts[:field]  || Array.new(9) { 0 }
      @turn    = opts[:turn]   || 1
    end

    #  Helper to determine whether it is the provided player's turn
    def player_moves_next?(n); @turn==n; end

    # increment turn
    def next_turn!
      #@turn += 1
      #@turn %= 3

      if player_moves_next?(2)
        @turn = 1  
      else
        @turn = 2
      end
    end

    #
    #  Output the current state of the board. Optionally accepts a mapping to
    #  instruct the printer how to translate the integer-valued board elements.
    #
    #
    def pretty(value_map=[' ','X','O'])
      txt = StringIO.new

      matrix.each_with_index do |row, n|
        txt << row.map do |value|
          mark = value_map[value]
          line = " #{mark} "
          line
        end.join('|') << "\n"

        # draw a line between each row
        txt << "-"*((3*3)+(2)) << "\n" unless n == matrix.length-1
      end

      txt.rewind
      txt.read
    end


    #
    #  Dimension-indirection helper to provide direct access to values in
    #  the underlying board matrix.
    #
    def get(x,y)
      # p @matrix
      # puts "--- attempting to find value at row #{x}, column #{y}"
      value = matrix[x][y]
      # puts "--- returning #{value}"
      value
    end


    def set(x,y,value)
      i = x*3 + y
      @field[i] =  value
    end

    #
    #
    #  A public facility for placing a move, with a sanity check for not
    #  marking the same cell twice.
    #
    #
    def inscribe!(position, mark=@turn)
      x,y = position[0], position[1]
      if get(x,y) != 0
        raise ArgumentError.new("may not mark a board position ([#{x},#{y}]) already marked (as #{get(x,y)})")
      end
      set x, y, mark
    end


    def erase!(p)
      raise ArgumentError.new("erasing an empty position") if get(p[0],p[1]) == 0
      set(p[0],p[1],0)
    end




    #
    #  Iterator yielding the elements of the board.
    #
    #def each
    #  @field.each
#      matrix.each_with_index do |row|
#        row.each_with_index do |value|
#          yield value
#        end
#      end
    #end



    #
    #  Iterator yielding the elements of the board matrix in order, and
    #  also yielding the position as the first and second elements of an
    #  array respectively.
    #
    def each_with_position
      matrix.each_with_index do |row, x|
        row.each_with_index do |value, y|
          yield [value, [x,y]]
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
      rows_columns_and_diagonals.each do |line|
        return true if line.uniq.length == 1 and line.uniq != [0]
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

      rows_columns_and_diagonals.each do |line|
        if line.first != 0
          return line.first if line.uniq.size == 1
        end
      end

      # since we would have complained if we've been invoked when the game couldn't be called yet
      # the game appears to be a draw
      0
    end



    #
    #  Provide collection of legal 'next' board states
    #
    # TODO optimize; first thought (to make this an iterator) is on the money
    #      we can just use THIS board, and inscribe/erase as necessary
    # =>   this is crazy expensive memory-wise, accordingly.
    # =>   probably won't help the speed much at all, think we'll need some a/b for that.
    def legal_next_states #(player)
      raise StandardError.new("cannot predict legal next game board configurations once game is over") if done?
      unmarked_positions.collect do |position|
        board = Board.new :field => @field.clone, :turn => @turn
        board.inscribe! position #, @turn #player
        board.next_turn!
        board
      end
    end


    def matrix
      f = @field
      [[f[0],f[1],f[2]],
       [f[3],f[4],f[5]],
       [f[6],f[7],f[8]]]
    end

    #
    #  Internal helper to determine whether there are any empty
    #  spaces still left on the board.
    #
    def board_filled
      @field.each { |v| return false if v == 0 }
      true
    end 

    #
    #  Internal helper for gathering the diagonal elements.
    #
    def diagonals
      [ (0..2).collect { |i| matrix[i][i]    },
        (0..2).collect { |i| matrix[i][2-i] } ]
    end

    #
    #  Internal helper for iterating over both rows and columns.
    #  We can get these fairly directly by enumerating the board
    #  and its transposition.
    #  
    #  The diagonals are a bit trickier; I think it's probably
    #  just to do it in the pseudo-general way above.
    #
    def rows_columns_and_diagonals
      matrix + matrix.transpose + diagonals #.collect
    end


  end # end Board
end # end TicTacToe