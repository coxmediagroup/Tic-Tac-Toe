
class Array
  def uniq_by(&blk)
    transforms = []
    self.select do |el|
      should_keep = !transforms.include?(t=blk[el])
      transforms << t
      should_keep
    end
  end
end

module TicTacToe
  class Tree
    
    def initialize(state=State.new, observe=StateObserver.new)
      @state = @root = state
      @observe = observe

      # puts "=== New tree created, with root"
      # pretty_print @root
    end

    def current_state;    @state;   end
    def current_observer; @observe; end

    def generate_successors(state=current_state, observe=current_observer,depth=0)
      puts "--- generate successors [depth=#{depth}]"
      observe.pretty_print state
      return if observe.terminal? state # r depth < MAX_DEPTH
      observe.open_positions(state).each do |position|
        successor = State.new(state.board.dup)
        successor.board[position] = state.current_player
        successor.current_player =  3-state.current_player
        generate_successors(successor, observe, depth-1) unless observe.terminal? successor
        state.successors[position] = successor
      end
    end


    MAX_DEPTH = -3
    #
    #
    #
    def collect_successors(state=current_state,observe=current_observer,depth=0)
      puts "--- collect successors [depth=#{depth}, terminal=#{observe.terminal? state}]"
      successors = [state]
      return successors if observe.terminal? state or depth < MAX_DEPTH
      for successor in state.successors.values
        collect_successors(successor,observe,depth-1).each do |n|
          successors << n
        end
      end
      successors.uniq_by { |s| s.board }
    end

    #
    # recursive helper to visually debug the state of the tree (will build the tree from the given state if need be)
    #
#    def pretty_print(state=@state, observe=@observe,depth=0)
#      puts
#      puts "----------- state at depth #{depth} --------------"
#      puts
#      puts
#      observe.pretty_print(state)
#      generate_successors(state) if state.successors.empty? and not observe.terminal? state
#      depth = depth - 1
#      for successor in state.successors.values
#        pretty_print(successor,observe,depth)
#      end
#    end
  end
end
