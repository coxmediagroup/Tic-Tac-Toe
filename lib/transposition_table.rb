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
  #
  module TranspositionTable
    


    #
    #  When this module is included into a class, alias the default 'value' function;
    #  we'll invoke it ourselves when we are sure we need it (i.e., it's not already
    #  in the transpositions table.)
    #
    #  Similarly, ensure that wheneve we are intending to determine open
    #  positions on the board, that we only look up transpositionally unique
    #  positions.
    #
    def self.included(base)
      
      # alias :value :evaluate_with_transposition_table

      # self.
      # alias :open_positions :transpositionally_unique_open_positions

      base.class_eval do
        # alias :_value :value
        alias :_open_positions :open_positions


        #
        #
        #   Evaluate open positions, and compute the transpositionally unique
        #   subset. Override the existing "open_positions" methods to do so.
        #
        def open_positions(state)
          transpositionally_unique = {}
          open = _open_positions(state)
          open.each do |i|
            s = state.successor(i)
            unique = true
            transpositionally_unique.keys.each do |state_already_added|
              unique = false if are_transpositionally_isomorphic?(s, state.successor(state_already_added), self)
            end
            transpositionally_unique[i] = s if unique
          end
          moves = transpositionally_unique.keys
          moves
        end
      end
    end

    IDENTITY        = lambda { |i| i }
    TRANSPOSE       = lambda { |i| i.transpose }

    INVERSE         = lambda { |i| i.reverse }
    INVERSE_HORIZ   = lambda { |i| i.transpose.reverse.transpose }
    
    ROTATE          = lambda { |i| i.reverse.transpose }
    ROTATE_180      = lambda { |i| i.reverse.transpose.reverse.transpose }
    ROTATE_CCW      = lambda { |i| i.transpose.reverse }

   


    #
    #   Performs a transformation on the state provided, yielding a
    #   new state with the transformed board.
    #
    def apply_transformation(txform, matrix)
     txform.call(matrix).flatten
     #State.new(new_board, state.current_player)
    end

    #
    #    Iterator over the transpositions of a particular state.
    #
    #
    def each_transposition(state, observe=StateObserver.new)
      m = observe.matrix(state)
      [ IDENTITY, TRANSPOSE, INVERSE, ROTATE, INVERSE_HORIZ, ROTATE_CCW, ROTATE_180
      ].each do |txf|
        yield State.new(apply_transformation(txf, m), state.current_player)
      end
    end

    #
    #  Determine whether two states are transpositionally isomorphic
    #
    def are_transpositionally_isomorphic?(state, another_state, observer)
      each_transposition(state, observer) do |transpose|
        return true if transpose.board == another_state.board
      end
      false
    end



  end
end
