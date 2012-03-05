#
#  specified class:  TranspositionTable
#  extends:          --
#  module:           TicTacToe
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe

  #
  #   Provides transposition-lookup and recognition services.
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
      
      base.class_eval do
        alias :_open_positions :open_positions


        #
        #   Evaluate open positions, and compute the transpositionally unique
        #   subset. Override the existing "open_positions" methods to do so.
        #
        def open_positions(state)
          open = _open_positions(state)
          transpositionally_unique = {
            open.first => matrix(state.successor(open.first)) }

          # drop the first (added by default) position
          open.shift

          open.each do |i|
            s = state.successor(i)
            m = matrix(s)

            unique = true
            
            transpositionally_unique.keys.each do |state_already_added|
              other_m = transpositionally_unique[state_already_added]
              if are_transpositionally_isomorphic?(m, other_m)
                unique = false
                break
              end
            end

            next if not unique
            transpositionally_unique[i] = m
          end
          moves = transpositionally_unique.keys
          moves
        end
      end
    end

    #
    #   Transposition procs.
    #
    IDENTITY        = Proc.new { |i| i }
    TRANSPOSE       = Proc.new { |i| i.transpose }

    INVERSE         = Proc.new { |i| i.reverse }
    INVERSE_HORIZ   = Proc.new { |i| i.transpose.reverse.transpose }
    
    ROTATE          = Proc.new { |i| i.reverse.transpose }
    ROTATE_180      = Proc.new { |i| i.reverse.transpose.reverse.transpose }
    ROTATE_CCW      = Proc.new { |i| i.transpose.reverse }

    TRANSPOSITIONS = [ TRANSPOSE, INVERSE, INVERSE_HORIZ,
                       ROTATE, ROTATE_180, ROTATE_CCW ]
    TRANSPOSITIONS_WITH_IDENTITY = TRANSPOSITIONS + [ IDENTITY ]

    #
    #   Performs a transformation on the state provided, yielding a
    #   new state with the transformed board.
    #
    def apply_transformation(txform, matrix)
     txform.call(matrix)
    end

    #
    #    Iterator over the transpositions of a particular state natrux.
    #
    #
    def each_transposition(matrix, include_identity = false)
      (include_identity ? TRANSPOSITIONS_WITH_IDENTITY : TRANSPOSITIONS).each do |txf|

        # pass each transformed matrix back up
        yield apply_transformation(txf,matrix)

      end
    end

    #
    #  Determine whether two state matrices are isomorphic up to transpositions.
    #
    def are_transpositionally_isomorphic?(state_matrix, another_state_matrix, include_identity = false)
      isomorphic = false
      each_transposition(state_matrix, include_identity) do |transpose|
        if transpose == another_state_matrix
          isomorphic = true
          break
        end
      end
      isomorphic
    end
  end
end
