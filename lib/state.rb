#
#  specified class:         State
#  extends:                 --
#  module:                  TicTacToe
#
#   description:
#
#   The state class encapsulates a node in a game tree -- a snapshot
#   of a game configuration including the inscriptions on the game
#   board and the current player.
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#

module TicTacToe
  class State
    
    attr_accessor :board, :current_player, :successors

    #
    #   A new state can be created with just an array of values (0-space,1-X, 2-O)
    #   but also optionally takes the player up.
    #
    def initialize(field = initial_field, current_player=1)
      @board          = field
      @current_player = current_player
      @successors     = {}
    end


    #
    #    Switch to the next player
    #
    def toggle_player
      if @current_player == 1
        @current_player = 2
      else
        @current_player = 1
      end
    end


    #
    #  Determine whether the game board is empty
    #
    def empty?; @board == initial_field; end


    #
    #  Construct a new State object with the given index marked and
    #  the current player toggled. Raises a StandardError if the successor
    #  index isn't empty.
    #
    def successor(n)
      # puts "-- attempting to generate successor state to current state, moving at #{n}: "
      # StateObserver.new.pp(self)
      raise StandardError.new("invalid successor index '#{n}' provided") if n.nil? or @board[n] != 0
      succ = State.new(@board.dup, @current_player)
      succ.board[n] = @current_player
      succ.toggle_player
      succ
    end


    #
    #   Determine whether this state has a legal successor at the provided
    #   position.
    #
    #
    def has_legal_successor?(n)
      successor(n)
      true
    rescue
      false
    end

    private

    def initial_field; Array.new(9) {0}; end


  end
end
