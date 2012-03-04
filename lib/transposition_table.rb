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


    #
    #  When this module is included into a class, alias the default 'value' function;
    #  we'll invoke it ourselves when we are sure we need it (i.e., it's not already
    #  in the transpositions table.)
    #
    #  Similarly, ensure that wheneve we are intending to determine open
    #  positions on the board, that we only look up transpositionally unique
    #  positions.
    #
    def included
      alias :_value :value
      alias :value :evaluate_with_transposition_table

      alias :_open_positions :open_positions
      alias :open_positions :transpositionally_unique_open_positions
    end

    #
    #  Override the value returned by default from the strategy with the
    #  cached value from the transposition table, if present (memorize
    #  otherwise.)
    #
    def evaluate_with_transposition_table(state,player=1,depth=0,alpha=-INFINITY,beta=INFINITY)
      return lookup(state) if depth < -4 and recognized? state
      val = _value(state,player,depth,alpha,beta)
      memorize(state,val)
      val
    end



    #
    #
    #   Evaluate open positions, and compute the transpositionally unique
    #   subset. Override the existing "open_positions" methods to do so.
    #
    def transpositionally_unique_open_positions(state)
      transpositionally_unique = {}
      _open_positions(state).each do |n|
        transpositionally_unique = true
        transpositionally_unique.keys.each do |state_already_added|
          transpositionally_unique = false if are_transpositionally_isormophic?(state, state_already_added)
        end
        transpositionally_unique[n] = state.successor(n) if transpositionally_unique
      end
      transpositionally_unique.keys
    end
    
    # TODO override open_positions to only show topologically
    #      UNIQUE successors -- should really help early game, when there's
    #      really only two or three moves to look at, but it 'feels' like
    # =>   8 to the CPU without knowing about the transpositions table



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
    ROTATE_CCW      = IDENTITY_MATRIX.transpose.reverse.flatten

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
      each_transposition(state) do |state_transform|
        @@transposition_table[hash(state_transform)] = value
      end
    end


    #
    #     Directly pulls a value from the lookup table based on the hash
    #     of the provided state.
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
      [ TRANSPOSE, INVERSE, ROTATE, ROTATE_CCW, INVERSE_HORIZ ].each do |transformation|
        yield apply_transformation(transformation, state)
      end
    end

    #
    #  Determine whether two states are transpositionally isomorphic
    #
    def are_transpositionally_isomorphic?(state, another_state)
      each_transposition(state) do |state_transform|
        return true if state_transform.board == another_state.board
      end
      false
    end


    #
    #     Class helper method to clear the transpositions table.
    #
    def TranspositionTable.clear!
      @@transpositions_table = {}
    end

  end
end
