#
#  class:                   Tree
#  extends:                 --
#  module:                  TicTacToe
#
#   description:
#
#   Constructs the game state tree and can assemble an iterator for the
#   full set of possible legal future states from a given board configuration.
#
#   In passing I want to note that, looking forward, constructing
#   the full tree in advance is technically unnecessary, and we may want to
#   de-factor this back out (once transpositions and a/b are working).
#   On the other hand, hashes could speed this construction up significantly;
#   transposition tables as well, etc.
#
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#
#
module TicTacToe

  class Tree
    
    def initialize(state=State.new, observe=StateObserver.new)
      @state = @root = state
      @observe = observe
    end

    def current_state;    @state;   end
    def current_observer; @observe; end

    def generate_successors(state=current_state, observe=current_observer, depth=0)
      return if observe.terminal? state
      observe.open_positions(state).each do |position|
        successor = State.new(state.board.dup)
        successor.board[position] = state.current_player
        successor.current_player =  3-state.current_player
        generate_successors(successor, observe, depth-1) unless observe.terminal? successor
        state.successors[position] = successor
      end
    end


    MAX_DEPTH = -2
    #
    #   iterate over future legal states
    #
    def each_successor(state=current_state, observe=current_observer, depth=0)      
      if observe.terminal? state or depth <= MAX_DEPTH
        yield state
        return
      end

      state.successors.values.each do |successor|
        yield successor if depth == 0
        each_successor(successor,observe,depth-1) { |s| yield s }
      end
    end
  end
end
