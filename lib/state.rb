module TicTacToe

  #
  #
  #  technically this could be done as 8 bits, i.e., a single byte!
  #
  class State
    
    attr_accessor :board, :current_player, :successors

    def initialize(field = initial_field, current_player=1)
      @board          = field
      @current_player = current_player
      @successors     = {}
    end


    def toggle_player
      if @current_player == 1
        @current_player = 2
      else
        @current_player = 1
      end
    end


    def empty?; @board == initial_field; end


    private

    def initial_field; Array.new(9) {0}; end


  end
end
