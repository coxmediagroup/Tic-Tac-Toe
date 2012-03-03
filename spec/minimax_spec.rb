#
#   Specifications for the Minimax class.
#


require 'minimax'
require 'state_observer'
require 'state'
require 'tree'

module TicTacToe


#  describe Minimax, "should short-circuit the first move, selecting 1" do
#    subject { Minimax.best_move(State.new) }
#    it { should be 0 }
#  end

  describe Minimax, "should evaluate final states" do
    before(:each) { @observes = StateObserver.new }

    it "should evaluate as an observer, but magnifying to +/- infinity if the depth is 0 or -1" do

      # @empty_state = State.new
      depth = 1
      @draw_state  = State.new [
        1,2,1,
        2,1,2,
        2,1,2
      ]

#      Minimax.value(
 #       @draw_state, 1, depth, @observes).should == 0

      @player_one_win_state = State.new [
        1,1,1,
        2,0,2,
        1,2,1
      ]

      depth = 1
 #     Minimax.value(
#        @player_one_win_state, 1, depth, @observes).should == 1
      
      depth = 0
      Minimax.value(
        @player_one_win_state, 1, depth, @observes).should == INFINITY

#      @player_two_win_state = State.new [
#        1,0,1,
#        2,2,2,
#        1,2,1
#      ]
#
#      depth = 1
#      Minimax.value(
#        @player_two_win_state, 1, depth, @observes).should == -1
#      depth = 0
#      Minimax.value(
#        @player_two_win_state, 1, depth, @observes).should == -INFINITY


    end
  end

  describe Minimax, "evaluates states recursively" do
  
    before(:each) { @observes = StateObserver.new }

    #
    #  sanity check the minimax implementation
    #
    it "should rank available moves" do

      player = 1
      @state = State.new [
        2,0,0,
        1,1,0,
        0,2,0
      ]
      Minimax.best_move(@state, player, @observes).should == 5

      
      @state = State.new [
        0,0,2,
        0,1,2,
        0,0,0
      ]
      Minimax.best_move(@state, player, @observes).should == 8



      @state = State.new [
        2,0,0,
        1,0,0,
        0,1,2
      ]
      Minimax.best_move(@state, player, @observes).should == 4


      @state = State.new [
        2,0,0,
        0,0,1,
        2,1,0
      ]
      Minimax.best_move(@state, player, @observes).should == 3


      @state = State.new [
        2,1,0,
        0,0,1,
        2,0,0
      ]
      Minimax.best_move(@state, 1, @observes).should == 3

      @state = State.new [
        1,2,0,
        0,2,1,
        0,0,0
      ]
      Minimax.best_move(@state, 1, @observes).should == 7

    end
  end


  describe Minimax, "provides optimal play" do
    it "should play every legal board position to a win or draw" do
      @observe = StateObserver.new
      @tree = Tree.new
      puts "--- generating successors, just a moment..."
      @tree.generate_successors
      puts "--- done!"

      @tree.each_successor do |state|
        3.times do
          puts '*'*80
        end
        
        @state = State.new(state.board, state.current_player)

        first_player = @state.current_player
        second_player = 3 - first_player

        until @observe.terminal? @state

          puts "==== player #{first_player} considering board state"
          @observe.pretty_print @state
          player_one_move = Minimax.best_move(@state, first_player, @observe)
          puts "--- player #{first_player} has elected to move at #{player_one_move}"
          @state = @state.successors[player_one_move]

          unless @observe.terminal? @state
            puts "==== player #{second_player} considering board state"
            @observe.pretty_print(@state)
            player_two_move = Minimax.best_move(@state, second_player, @observe)
            puts "--- player #{second_player} has elected to move at #{player_two_move}"
            @state = @state.successors[player_two_move]
            @observe.pretty_print @state
          end
        end

        winner = @observe.winner @state

        puts
        puts
        puts "========== WINNER: #{winner}" if winner > 0
        puts "========== DRAW" if winner == 0
        puts
        puts
        # first player must win or draw
        (winner == 1 or winner == 0).should be true
      end

    end

  end

end