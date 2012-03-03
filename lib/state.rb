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


    private

    def initial_field; Array.new(9) {0}; end


  end
end
