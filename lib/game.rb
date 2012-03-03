#
#  class:         Game
#  extends:       --
#  module:        TicTacToe
#
#   description:
#
#   Provides a Tic-Tac-Toe game engine that plays interactively with a human
#   being. Application entrypoint.
#
#   The difficulty is currently not scalable, and is an exhaustive exercise,
#   so have "fun" -- you shouldn't be able to win.
#
#
#   feature wishlist:
#       - scalable difficulty / enforced time limits on computation
#       - support arbitrary board sizes
#       - support 2+ opponents
#       - playable via local network and/or web
#
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#
$:.unshift("../lib")

require 'stringio'

require 'state'
require 'tree'
require 'state_observer'
require 'minimax'

module TicTacToe
  class Game

    attr_accessor :tree, :state, :observer

    def initialize
      @state   = @root = State.new
      @observe = StateObserver.new
      @tree    = Tree.new(@state)
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

      puts "--- Welcome! You'll enter your moves as follows: "
      puts
      @observe.pretty_print(about_state, one_to_nine.map(&:to_s))
      puts
      puts "--- So, you'll just enter 1 for the top-left column, 2 for top-center; 9 for the bottom right, etc."
      
      5.times { puts }

    end

    #
    #   play a game with the computer
    #
    def play(first_time=true)
      about
      puts
      puts "=== Performing setup. (Please wait, this may take a minute or two.)"
      @tree.generate_successors(@root) if first_time
      @state = @root
      puts "--- Ok, great. Thanks for waiting. Let's play!"
      @observe.pretty_print @state
      raise StandardError("state was unexpectedly nil?!") if @state.nil?
      until @observe.terminal? @state
        puts
        puts "=== Computer player considering move, please wait..."
        # puts "--- options: "
        # p @state.successors.keys
        cpu_move = Minimax.best_move(@state, 1, @observe)
        @state = @state.successors[cpu_move]
        puts "--- CPU has elected to inscribe #{cpu_move}."
        @observe.pretty_print @state

        # move human
        unless @observe.terminal? @state

            human_move = ''
            puts
            puts "--- It's your turn! Please enter your move (1-9) [e.g., #{@state.successors.keys.join(',')}]: "
            human_move = gets.chomp until human_move.match(/^[1-9]$/) and @state.successors.has_key?(human_move.to_i-1)
            @state = @state.successors[human_move.to_i-1]

        end
      end

      puts "=== player #{@observe.winner(state)} is victorious."
      puts "play again? "
      play(false) if gets.chomp.downcase.slice(0).chr == 'y'
    end
  end
end

TicTacToe::Game.new.play if __FILE__ == $0