#
#     A group of shared focused behavior descriptions for
#     gameplaying strategies subclassing AbstractStrategy class.
#

module TicTacToe
  shared_examples_for "a strategy" do

    before(:each) do
      @ai = described_class.new
      @mock_game = MockGame.new(@ai)
      @state = State.new
    end

    it "should rank a several 'clear' optimal moves" do
    puts '---'
      player = 1
      states_and_best_moves = [
        [[ 2,0,0, 1,1,0, 0,2,0 ], 5],
        [[ 0,0,2, 0,1,2, 0,0,0 ], 8],
        [[ 2,0,0, 1,0,0, 0,1,2 ], 4],
        [[ 1,2,0, 0,2,1, 0,0,0 ], 7],
        [[ 2,1,0, 0,0,1, 2,0,0 ], 3],
        [[ 2,0,0, 0,0,1, 2,1,0 ], 3]
      ]

      for state, best_move in states_and_best_moves
        @state = State.new(state)
        @ai.best_move(@state, player, true).should be best_move
      end
      puts "---"
    end

    it "should play to a win/draw mock games for all successors of a given state" do
      draws, wins, losses = @mock_game.play_immediate_successors(@state,true)

      losses.should be 0
      draws.should be >= 0
      wins.should be >= 0
    end

    it "should play to a win/draw mock games for all successors of successors" do
      draws, wins, losses = @mock_game.play_successors(@state, 2,true)

      losses.should be 0
      draws.should be >= 0
      wins.should be >= 0
    end
  end
end