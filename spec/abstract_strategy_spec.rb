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
#
module TicTacToe


  #
  #   Focused descriptions for gameplaying algorithms.
  #
  shared_examples_for "a strategy" do

    before(:each) do
      @ai = described_class.new
      @mock_game = MockGame.new(@ai)
      @state = State.new

      @debug = false
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



  #
  #     Focused behavior descriptions for optimizing augmentations to
  #     gameplaying algorithms.
  #
  shared_examples_for 'an optimization' do
    describe "it should integrate safely into an existing algorithm" do
      before(:each) do
        @optimized = described_class.new
        @unoptimized = described_class.superclass.new 

        @optimized_mock_game = MockGame.new(@optimized)
        @unoptimized_mock_game = MockGame.new(@unoptimized)

        @state = State.new

        @debug = false
      end

      it "should select 'clearly' optimal moves" do
        # sanity check
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
          @optimized.best_move(@state, player, @debug).should be best_move
        end
      end

      it "should play mock games against itself to a win/draw from every legal starting position" do
        # pass 1
        @state = State.new
        draws, wins, losses = @optimized_mock_game.play_immediate_successors(@state, @debug)

        losses.should be 0
        draws.should be >= 0
        wins.should be >= 0
      end

      it "should play mock games against itself to a win/draw from every successor of every legal starting position" do
        # pass 2
        @state = State.new
        draws, wins, losses = @optimized_mock_game.play_successors(@state, 1, @debug)

        losses.should be 0
        draws.should be >= 0
        wins.should be >= 0
      end

      it "should show significant (>%5) improvement over unaugmented algorithm performance" do
        n = 1
        unoptimized_realtime = Benchmark.realtime do
          n.times do
            draws, wins, losses = @unoptimized_mock_game.play_immediate_successors(@state, @debug)
            losses.should be 0
            draws.should be >= 0
            wins.should be >= 0
          end
        end
        puts "--- unoptimized realtime: #{unoptimized_realtime}" if @debug

        optimized_realtime = Benchmark.realtime do
          n.times do
            draws, wins, losses = @optimized_mock_game.play_immediate_successors(@state, @debug)
            losses.should be 0
            draws.should be >= 0
            wins.should be >= 0
          end
        end

        puts "--- optimized realtime: #{optimized_realtime}" if @debug

        improvement = optimized_realtime / unoptimized_realtime

        puts "=== improvement #{improvement}"
        improvement.should be <= 0.95


      end
    end
  end
end