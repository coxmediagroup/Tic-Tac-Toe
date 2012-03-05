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
  #   TODO investigate 
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
        #   Begin the cache at states at depth of -2 or greater (successors
        #   of successor nodes and their subtrees) from the current point of view.
        #
        def reached_cache_depth?(depth); depth <= -4; end

        #
        #  Override the value returned by default from the base strategy with the
        #  cached value from the cache, if present (memorize otherwise.)
        #
        def value(state,player=1,depth=0,alpha=-INFINITY,beta=INFINITY,color=1)
          return endgame_score(state,player,depth) if terminal?(state)

          unless reached_cache_depth?(depth)
            each_transposition(state,self) do |transpose|
              val = recognized?(transpose, depth)
              return val unless val == false
            end
          end

          score = _value(state,player,depth,alpha,beta,color)
          memorize(state,score,depth) if reached_cache_depth?(depth)
          score
        end # end base.value [dynamically overriden]
      end # end base.class_eval
    end # end InMemoryStateValueCache.included(base)


    #
    #  Determine whether a particular state is entered into the table.
    #  Return the value if found.
    #
    def recognized?(state, depth=0)
      @@state_value_table ||= {}
      each_transposition(state,self) do |transpose|
        if @@state_value_table.keys.include? hash(transpose,depth)
          return @@state_value_table[hash(transpose, depth)]
        end
      end
      false
    end

    #
    #
    #     Memorize the value of the provided state.
    #
    def memorize(state, value, depth=0)
      raise StandardError.new("cannot enter a nil value") if value.nil?
      @@state_value_table ||= {}
      @@state_value_table[hash(state, depth)] = value
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
    def hash(state,depth)
      key = state.board.hash.to_s + state.current_player.to_s + depth.abs.to_s
      key = key.to_i
      key
    end

  end # end module InMemoryStateValueCache
end
