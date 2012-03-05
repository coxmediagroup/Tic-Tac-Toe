#
#  class:         Game
#  extends:       StateObserver
#  module:        TicTacToe
#  author:        Joseph Weissman, <jweissman1986@gmail.com>
#
#
$:.unshift("./lib")

require 'stringio'

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
  #   Provides a Tic-Tac-Toe game engine that plays interactively with a human
  #   being. Application entrypoint.
  #
  #
  #   Feature wishlist:
  #       - scalable difficulty / enforced time limits on computation
  #       - support arbitrary board sizes
  #       - support 2+ opponents
  #       - playable via local network and/or web
  #
  class Game < StateObserver

    attr_accessor :tree, :state, :observer, :ai

    # which algorithm to utilize
    AI = AlphaBetaWithTranspositionTable

    def initialize
      @state   = @root = State.new
      @ai      = AI.new
    end

    #
    #   display an about message
    #
    def about
      zero_to_eight = Array.new(9) { |i| i   }
      one_to_nine = Array.new(9)   { |i| i+1 }

      about_state = State.new(zero_to_eight)

      puts '='*80
      puts
      puts "Tic Tac Toe".center(80)
      puts
      puts '='*80

      10.times { puts }

      puts "=== Welcome!"
      puts "--- Please enter your moves as follows: "
      puts
      pp(about_state, one_to_nine.map(&:to_s))
      puts
      puts "--- So, please indicate the top-left column as 1, the top-center as 2, the bottom right as 9; etc."
      
      5.times { puts }

    end

    #
    #   Play a game against the computer.
    #
    def play
      about
      puts
      @state = @root
      pp @state
      until terminal? @state
        puts
        puts "=== Computer player considering move, please wait..."
        cpu_move = @ai.best_move(@state, 1) 
        puts "--- CPU has elected to inscribe #{cpu_move}."
        @state = @state.successor(cpu_move)
        pp @state

        unless terminal? @state
          begin
            human_move = ''
            puts
            puts "--- It's your turn! Please enter your move (1-9):"
            human_move = gets.chomp until human_move.match(/^[1-9]$/)  and @state.has_legal_successor?(human_move.to_i - 1)

            @state = @state.successor(human_move.to_i-1)
          rescue StandardError => e



          end
          # ./lib/state.rb:59:in `successor': invalid successor index '3' provided (StandardError)

        end
      end

      puts "=== Player #{winner(state)} is victorious!"
      puts
      puts
      puts "Do you wish to challenge me again? (y/n)"
      play if gets.chomp.downcase.slice(0).chr == 'y'
    end
  end
end

TicTacToe::Game.new.play if __FILE__ == $0