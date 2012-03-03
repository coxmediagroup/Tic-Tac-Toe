#
#  class:         MinimaxSpec
#  extends:       --
#  module:        TicTacToe
#
#   description:
#
#   Provides a specification for the Minimax implementation powering the
#   engine.
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#
require 'minimax'
require 'state_observer'
require 'state'
require 'tree'

module TicTacToe

   # _=0,X=1,O=2
  describe Minimax, "should evaluate final states" do
    before(:each) { @observes = StateObserver.new }

    it "should evaluate as an observer, but magnifying to +/- infinity if the depth is 0 or -1" do
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

      depth = -3
      Minimax.value(
        @player_one_win_state, 1, depth, @observes).should == 1
      Minimax.value(
        @player_one_win_state, 2, depth, @observes).should == -1

      depth = 0
      Minimax.value(
        @player_one_win_state, 2, depth, @observes).should == -INFINITY
      Minimax.value(
        @player_one_win_state, 1, depth, @observes).should == INFINITY



    end
  end


  describe Minimax, "evaluates states recursively" do
  
    before(:each) { @observes = StateObserver.new }

    #
    #  sanity check the minimax implementation
    #
    it "should rank a several 'clear' optimal moves" do

      player = 1
      @state = State.new [
        2,0,0,
        1,1,0,
        0,2,0
      ]
      Minimax.best_move(@state, player, @observes).should be 5

      
      @state = State.new [
        0,0,2,
        0,1,2,
        0,0,0
      ]
      Minimax.best_move(@state, player, @observes).should be 8



      @state = State.new [
        2,0,0,
        1,0,0,
        0,1,2
      ]
      Minimax.best_move(@state, player, @observes).should be 4


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
      Minimax.best_move(@state, player, @observes).should == 3

      @state = State.new [
        1,2,0,
        0,2,1,
        0,0,0
      ]
      Minimax.best_move(@state, player, @observes).should == 7

      player = 2
      @state = State.new [
        0,2,1,
        1,1,2,
        0,0,0
      ]
      @state.current_player = 2
      Minimax.best_move(@state,player,@observes).should == 6
    end


=begin
    #
    # the data for the following test is from a diagram here: http://xkcd.com/832/
    #

    it "should match XKCD's optimal Tic-Tac-Toe maps" do
      @state = State.new [
        1,0,0,
        0,0,0,
        0,0,0
      ]
      Minimax.best_move(@state, 2, @observes).should == 4

      @state = State.new [
        1,0,0,
        0,2,0,
        0,0,0
      ]
      Minimax.best_move(@state, 1, @observes).should == 8

      @state = State.new [
        1,0,0,
        0,2,0,
        0,0,1
      ]
      Minimax.best_move(@state, 2, @observes).should == 7
    end
=end
  end


  describe Minimax, "provides optimal play" do


    it "should play against itself on every legal state up to round 2 to a win or draw" do
      @observe = StateObserver.new
      @tree = Tree.new
      puts "--- generating successors, just a moment..."
      @tree.generate_successors
      puts "--- done! playing games..."

      @tree.each_successor do |state|
        print '.'
#        3.times do
#          puts '*'*80
#        end
        
        @state = State.new(state.board, state.current_player)

        first_player = @state.current_player
        second_player = 3 - first_player

        until @observe.terminal? @state

#          puts "==== player #{first_player} considering board state"
#          @observe.pretty_print @state
          player_one_move = Minimax.best_move(@state, first_player, @observe)
#          puts "--- player #{first_player} has elected to move at #{player_one_move}"
          @state = @state.successors[player_one_move]

          unless @observe.terminal? @state
#            puts "==== player #{second_player} considering board state"
#            @observe.pretty_print(@state)
            player_two_move = Minimax.best_move(@state, second_player, @observe)
#            puts "--- player #{second_player} has elected to move at #{player_two_move}"
            @state = @state.successors[player_two_move]
#            @observe.pretty_print @state
          end
        end

        winner = @observe.winner @state

#        puts
#        puts
#        puts "========== WINNER: #{winner}" if winner > 0
#        puts "========== DRAW" if winner == 0
#        puts
#        puts
        # first player must win or draw
        (winner == 1 or winner == 0).should be true
      end

      puts 'done'

    end

  end

end