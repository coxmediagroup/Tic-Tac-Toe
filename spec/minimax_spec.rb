#
#   Specifications for the Minimax class.
#


require 'minimax'
require 'state_observer'
require 'state'
require 'tree'

module TicTacToe


  describe Minimax, "should short-circuit the first move, selecting 1" do
    subject { Minimax.best_move(State.new) }
    it { should be 0 }
  end

  describe Minimax, "should evaluate final states" do
    before(:each) { @observes = StateObserver.new }

    it "should evaluate as an observer, but magnifying to +/- infinity if the depth is 0" do

      # @empty_state = State.new
      depth = 1
      @draw_state  = State.new [
        1,2,1,
        2,1,2,
        2,1,2
      ]

      Minimax.value(
        @draw_state, 1, depth, @observes).should == 0

      @player_one_win_state = State.new [
        1,1,1,
        2,0,2,
        1,2,1
      ]

      depth = 1
      Minimax.value(
        @player_one_win_state, 1, depth, @observes).should == 1
      
      depth = 0
      Minimax.value(
        @player_one_win_state, 1, depth, @observes).should == INFINITY

      @player_two_win_state = State.new [
        1,0,1,
        2,2,2,
        1,2,1
      ]

      depth = 1
      Minimax.value(
        @player_two_win_state, 1, depth, @observes).should == -1
      depth = 0
      Minimax.value(
        @player_two_win_state, 1, depth, @observes).should == -INFINITY


    end
  end

  describe Minimax, "evaluates states recursively" do
  
    before(:each) { @observes = StateObserver.new }

    it "should rank available moves" do

      player = 1
      @state = State.new [
        2,0,0,
        1,1,0,
        0,0,2
      ]
      Minimax.best_move(@state, player, @observes).should == 5

      
      @state = State.new [
        0,0,2,
        2,1,2,
        1,2,0
      ]
      Minimax.best_move(@state, player, @observes).should == 8



      @state = State.new [
        2,1,0,
        1,0,0,
        0,0,2
      ]
      Minimax.best_move(@state, player, @observes).should == 4

    end

    describe Minimax, "provides optimal play" do
      it "should win/draw if it gets to start" do
        @observe = StateObserver.new
        @state = State.new
        @tree = Tree.new(@state)

        puts '--- generating subtrees'
        @tree.generate_successors

        until @observe.terminal? @state

          puts "==== player 1 considering board state"
          @observe.pretty_print @state

          player_one_move = Minimax.best_move(@state, 1, @observe)
          puts "--- player 1 has selected to move at #{player_one_move}"
          @state = @state.successors[player_one_move]
          puts "--- state after player 1's move"
          @observe.pretty_print(@state)

          unless @observe.terminal? @state
            puts "==== player 2"
            player_two_move = Minimax.best_move(@state, 2, @observe)
            @state = @state.successors[player_two_move]
            @observe.pretty_print @state
          end
          
        end

        @observe.winner(@state).should be 0 or 1

      end
    end

    it "should play every legal board position (until turn 6) to a win or draw" do
      @observe = StateObserver.new
      @tree = Tree.new
      puts "--- about to generate successors"
      @tree.generate_successors
      puts "--- done!"
      @tree.collect_successors do |state|
        puts "-----------------"
        until @observe.terminal? state
          puts "==== player 1"
          player_one_move = Minimax.best_move(state, 1, @observe)
          state = state.successors[player_one_move]

          @observe.pretty_print state

          unless @observe.terminal? state
            puts "==== player 2"
            player_two_move = Minimax.best_move(state, 2, @observe)
            state = state.successors[player_two_move]
            @observe.pretty_print state
          end
        end

        @observe.winner(state).should be 0 or 1
      end
    end
  end
end