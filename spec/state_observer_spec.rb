#
#  specified class:         StateObserver
#  extends:                 --
#  module:                  TicTacToe
#
#   description:
#
#   Provides a specification for the game state observer class in charge
#   of most of the business logic around inspection and analysis of
#   static board configuration.
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#

require 'state_observer'
require 'state'

module TicTacToe
  describe StateObserver do
    before(:each) do
      @observes = StateObserver.new

      @empty_state = State.new
      @draw_state  = State.new [
        1,2,1,
        2,1,2,
        2,1,2
      ]

      @player_one_win_state = State.new [
        1,1,1,
        2,0,2,
        1,2,1
      ]

      @player_two_win_state = State.new [
        1,0,1,
        2,2,2,
        1,2,1
      ]
    end

    it "should format the state matrix for display" do
      describe State, "displays a game state" do
        subject { StateObserver.new.pretty(State.new) }
        it { should == "   |   |   \n-----------\n   |   |   \n-----------\n   |   |   \n" }
      end
    end


    it "should collect open positions" do
      @observes.open_positions(@empty_state).should == Array.new(9) {|i|i}
      @observes.open_positions(@player_one_win_state).should == [4]
      @observes.open_positions(@player_two_win_state).should == [1]

      @observes.open_positions(State.new [
        0,0,0,
        0,1,2,
        0,0,0
      ]).should == [0,1,2,3,6,7,8]
    end

    it "should detect win/loss/draw conditions and rank them accordingly" do
      
      @observes.terminal?(@empty_state).should be false

      @observes.winner(@draw_state).should == 0
      @observes.evaluate(@draw_state, 1).should == 0
      @observes.evaluate(@draw_state, 2).should == 0
      @observes.terminal?(@draw_state).should be true

      @observes.winner(@player_one_win_state).should == 1
      @observes.evaluate(@player_one_win_state, 1).should == +1
      @observes.evaluate(@player_one_win_state, 2).should == -1
      @observes.terminal?(@player_one_win_state).should be true

      @observes.winner(@player_two_win_state).should == 2
      @observes.evaluate(@player_two_win_state, 1).should == -1
      @observes.evaluate(@player_two_win_state, 2).should == +1
      @observes.terminal?(@player_two_win_state).should be true
    end

  end

end