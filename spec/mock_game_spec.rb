#
#  specified class:  MockGame
#  extends:          --
#  module:           TicTacToe
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#

require 'state'
require 'state_observer'
require 'abstract_strategy'
require 'mock_game'
require 'alpha_beta'
require 'state'
require 'infinity'
require 'transposition_table'
require 'alpha_beta_with_transposition_table'

module TicTacToe
  #
  #   Provides a specification for the MockGame implementation which drives our
  #   core test cases for the algorithms.
  #
  describe MockGame, "manages a simulated tic-tac-toe game" do
    before(:each) do
      @state = State.new
      @mock_game = MockGame.new
    end



    it "should play a mock game" do
      # puts "======= single mock match"
      winner = @mock_game.play(@state, false)
      winner.should >= 0
      winner.should <= 1
    end


    it "should play mock games for all successors of a given state" do
      # puts "======= first round mock matches"
      draws, wins, losses = @mock_game.play_immediate_successors(@state, false)

      losses.should be 0
      draws.should be >= 0      
      wins.should be >= 0
    end


    it "should play mock games for all successors of successors" do
      # puts "======= second round mock matches"

      draws, wins, losses = @mock_game.play_successors(@state,1, false)
      puts "--- draws: #{draws} / wins: #{wins} / losses: #{losses}"
      
      losses.should be 0
      draws.should be >= 0
      wins.should be >= 0
    end
  end
end