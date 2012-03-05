#
#  specified class:         AbstractStrategy
#  extends:                 --
#  module:                  TicTacToe
#  author:                  Joseph Weissman, <jweissman1986@gmail.com>
#
#
#  description:
#
#     A group of shared focused behavior descriptions for gameplaying
#     algorithms or 'strategies' (subclassing AbstractStrategy class.)
#
#     Also includes shared descriptions for algorithm augmentations,
#     or 'optimizations' (mixins for subclasses of AbstractStrategy.)
#
module TicTacToe


  shared_examples_for "a strategy" do

    before(:each) do
      @ai = described_class.new
      @mock_game = MockGame.new(@ai)
      @state = State.new

      @debug = true
    end

    it "should rank several 'clear' optimal moves" do
      player = 1
      states_and_best_moves = [
        [[ 2,0,0, 1,0,0, 0,1,2 ], 4],
        [[ 2,0,0, 1,1,0, 0,2,0 ], 5],
        [[ 0,0,2, 0,1,2, 0,0,0 ], 8],
        [[ 1,2,0, 0,2,1, 0,0,0 ], 7],
        [[ 2,1,0, 0,0,1, 2,0,0 ], 3],
        [[ 2,0,0, 0,0,1, 2,1,0 ], 3]
      ]

      for state, best_move in states_and_best_moves
        @state = State.new(state)
        @ai.best_move(@state, player, @debug).should be best_move
      end
    end

    it "should play to a win/draw mock games for all successors of a given state" do
      draws, wins, losses = @mock_game.play_immediate_successors(@state, @debug)

      losses.should be 0
      draws.should be >= 0
      wins.should be >= 0
    end

    it "should play to a win/draw mock games for all successors of successors" do
      draws, wins, losses = @mock_game.play_successors(@state, 1, @debug)

      losses.should be 0
      draws.should be >= 0
      wins.should be >= 0
    end
    
  end



  shared_examples_for 'an optimization' do

    before(:each) do
      @optimized = described_class.new
      @unoptimized = described_class.superclass.new # .new

      @optimized_mock_game = MockGame.new(@optimized)
      @unoptimized_mock_game = MockGame.new(@unoptimized)

      @state = State.new


      @debug = false
    end

    it "should integrate safely into an existing algorithm" do
      describe @optimized.class, 'behaves like a strategy' do
        it_should_behave_like 'a strategy'
      end
    end

    it "should show significant (>%0.5) improvement over unaugmented algorithm performance" do

      # puts "--- unoptimized..."
      unoptimized_realtime = Benchmark.realtime do
        draws, wins, losses = @unoptimized_mock_game.play_immediate_successors(@state, @debug)
        losses.should be 0
        draws.should be >= 0
        wins.should be >= 0
      end

      # puts "--- optimized..."
      optimized_realtime = Benchmark.realtime do
        draws, wins, losses = @optimized_mock_game.play_immediate_successors(@state, @debug)
        losses.should be 0
        draws.should be >= 0
        wins.should be >= 0
      end

      puts "--- optimized realtime: #{optimized_realtime}" # if @debug
      puts "--- unoptimized realtime: #{unoptimized_realtime}" # if @debug

      # unoptimized_realtime.should be > optimized_realtime
      improvement = unoptimized_realtime / optimized_realtime
      improvement.should be >= 1.05

    end

  end
end