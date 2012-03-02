#
#  class:         Game
#  extends:       --
#  module:        TicTacToe
#
#   description:
#
#   Provides a Tic-Tac-Toe game engine.
#
#
#   Wishlist:
#       - support arbitrary board sizes
#       - support 2+ opponents
#       - playable via web (thinking Sinatra)
#
#
#  author: Joseph Weissman, <jweissman1986@gmail.com>
#
#
module TicTacToe
  class Game

    attr_accessor :board, :players
    
    #
    #   Game.new takes an options hash with the following possible parameters:
    #
    #     :size       size of the board in question
    #     :humans     number of human players (mutually exclusive with :players)
    #
    def initialize(opts={})

      puts "=== Performing setup..."
      @players = []

      player_count = opts[:player_count] || 2
      human_count  = opts[:humans]       || 1
      cpu_count    = player_count - human_count

      puts "--- Creating #{human_count} human players."
      human_count.times { |n| @players << HumanPlayer.new(n+1)                } if human_count > 0

      puts "--- Creating #{cpu_count} AI players."
      cpu_count.times   { |m| @players << MaximizingPlayer.new(m+human_count+1) } if cpu_count   > 0

      puts "--- Setup complete."
    end


    def play!
      puts "--- Let's go!"

      @board   = Board.new :size => @size

      until @board.done?
        @players.each do |player|
          puts board.pretty
          player.move(@board)
          break if @board.done?
        end
      end

      puts "--- Game complete!"
      puts
      puts @board.pretty
      puts
      puts

      if @board.winner == nil
        puts "--- The game was a draw."
      else
        puts "--- Player #{@board.winner} is victorious."
      end

      puts "--- Would you like to begin another game?"
      play! if gets.chomp.downcase.slice(0).chr == 'y'
    end

  end
end
