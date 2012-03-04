#
#  specified class:  TranspositionTable
#  extends:          --
#  module:           TicTacToe
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
  #
  #
  #   Provides transposition-lookup and recognition services.
  #
  module TranspositionTable
    include HashingProvider


    #### transpositions #########

    #
    #   My hunch is that this mechanism might just be cheaper than ruby's means of
    #   reversing/transposes arrays of arrays.
    #
    #   TODO benchmark idioms and compare
    #
    IDENTITY        = Array.new(9) { |i| i }
    IDENTITY_MATRIX = [[1,2,3],[4,5,6],[7,8,9]]
    TRANSPOSE       = IDENTITY_MATRIX.transpose.flatten
    INVERSE         = IDENTITY_MATRIX.reverse.flatten
    ROTATE          = IDENTITY_MATRIX.reverse.transpose.flatten

    INVERSE_HORIZ   = IDENTITY_MATRIX.transpose.reverse.transpose.flatten


    #
    #  Determine whether a particular state is entered into the transpositions
    #  table under the known transformations.
    #
    def recognized?(state)
      @@transposition_table ||= {}
      @@transposition_table.keys.include?(hash(state))
    end

    #
    #
    #     Memorize the value of the provided state.
    #
    def memorize(state, value)
      raise StandardError.new("cannot enter a nil value") if value.nil?
      @@transposition_table ||= {}
      @@transposition_table[hash(state)] = value
      for state_transform in transpose(state)
        @@transposition_table[hash(state_transform)] = value
      end
    end


    #
    #
    #
    def lookup(state)
      @@transposition_table[hash(state)]
    end


    #
    #   Performs a transformation on the state provided, yielding a
    #   new state with the transformed board.
    #
    def apply_transformation(txform, state)
     new_board = Array.new(9)
     state.board.each_with_index do |val, i|
       new_board[txform[i]-1] = val
     end
     State.new(new_board, state.current_player)
    end

    #
    #    Iterator over the transpositions of a particular state.
    #
    #
    def each_transposition(state)
      [ TRANSPOSE, INVERSE, ROTATE, INVERSE_HORIZ ].each do |transformation|
        yield apply_transformation(transformation, state)
      end
    end


    #
    #     Class helper method to clear the transpositions table.
    #
    def TranspositionTable.clear!
      @@transpositions_table = {}
    end

  end
end
