#
#  class:         InMemoryStateValueCache
#  extends:       --
#  module:        TicTacToe
#  author:        Joseph Weissman, <jweissman1986@gmail.com>
#
#
module TicTacToe
  #
  #   Provide a transposition-aware state => value cache for optimizing
  #   traversals and accelerating computation of sums over minimax subtrees.
  #
  module InMemoryStateValueCache
    #
    #     Perform augmentations to strategy business logic on inclusion.
    #     In particular we include a transposition table and override the
    #     value function to check the cache prior to recursion.
    #
    def self.included(base)
      base.class_eval do
        include TranspositionTable
        alias :_value :value

        #
        #  Override the value returned by default from the base strategy with the
        #  cached value from the cache, if present (else memoize.)
        #
        def value(state,player=1,depth=0,alpha=-INFINITY,beta=INFINITY,color=1)
          if depth < -4
            m = matrix(state)
            val = recognized?(m, player, depth, color)
            if val
              return val
            end
          end

          score = _value(state,player,depth,alpha,beta,color)

          memorize(m,player,depth,color,score) if depth < -4
          score
        end # end base.value [dynamically overriden]
      end # end base.class_eval
    end # end InMemoryStateValueCache.included(base)

    #
    #  Determine whether a particular state is entered into the table.
    #  Return the value if found.
    #
    def recognized?(matrix, player=1, depth=0, color=1)
      @@state_value_table ||= {}
      h = hash(matrix, player, depth, color)
      if @@state_value_table.keys.include? h
        return @@state_value_table[h]
      end
      false
    end

    #
    #     Memorize the value of the provided state.
    #
    def memorize(matrix, player=1, depth=0, color=1, value=nil)
      raise ArgumentError.new("pass in matrix directly") if matrix.is_a? State
      raise StandardError.new("cannot enter a nil value") if value.nil?
      @@state_value_table ||= {}
      each_transposition(matrix, true) do |transpose|
        h = hash(transpose, player, depth, color)
        @@state_value_table[h] = value
      end
    end

    #
    #   Remove all entries from the transpositions table.
    #
    #   (For preventing test case leakage.)
    #
    def clear_state_value_table!
      @@state_value_table ||= {}
      @@state_value_table = @@state_value_table.clear
    end

    def collect_state_values
      @@state_value_table
    end

    protected
    #
    #    Construct a unique hash per board configuration / player / depth
    #
    def hash(matrix,player=1,depth=0, color=1)
      # [ player, depth, matrix.flatten ].hash
      [ matrix.flatten, player, depth, color ].hash
    end
  end # end module InMemoryStateValueCache
end