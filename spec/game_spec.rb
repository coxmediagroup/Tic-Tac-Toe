require_relative '../classes/game'
require 'yaml'
require 'spec_helper'

RSpec.describe Game do
  before :each do
    @test_game = Game.new
  end
  
  it 'creates a new Game object with an empty game Board using Game.new' do
    the_board = @test_game.get_board.board_array
    expect( the_board.select{|s| s.include? ""}.size ).to eq the_board.size
  end
  
  it 'will set the board position using apply_move' do
    position_to_set = 5
    token_to_set = "0"
    @test_game.apply_move(position_to_set, token_to_set)
    expect( @test_game.get_board.board_array[position_to_set] ).to eq token_to_set
  end
  
  it 'will return nil instead of applying a move if the position is already taken using apply_move' do
    position_to_set = 5
    token_to_set = "0"
    @test_game.apply_move(position_to_set, token_to_set)
    expect( @test_game.apply_move(position_to_set, "1") ).to eq nil
  end
  
  it 'will make a game path into "threat" if the score is enemy:2 and other:0' do
    
  end
  
  it 'finds the right slot to fill for a win using find_best_move()' do
    @test_game = Game.new
    #load up the board to set the stage
    @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.enemy_token )
    @test_game.apply_move( "0", @test_game.my_token )
    @test_game.apply_move( "1", @test_game.my_token )  
    
    expect(@test_game.find_best_move).to eq 2
   end
   
   it 'finds the right slot to fill to block a threat using find_best_move()' do
     @test_game = Game.new
     #load up the board to set the stage
     @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.my_token )
     @test_game.apply_move( "2", @test_game.enemy_token )
     @test_game.apply_move( "6", @test_game.enemy_token )
    
     expect(@test_game.find_best_move).to eq 4
    end
    
    it 'selects center of board (4) if no threats and no wins and it\'s open using find_best_move()' do
      @test_game = Game.new
      #load up the board to set the stage
      @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.my_token )
      @test_game.apply_move( "2", @test_game.enemy_token )
      # @test_game.apply_move( "3", @test_game.enemy_token )
      @test_play = Play.new( game: @test_game, move: "3" , token: @test_game.enemy_token )
  
      expect(@test_game.find_best_move).to eq 4
    end
    
    it 'finds the common hit positions available for both players and takes the first open corner if available' do
      @test_game = Game.new
      #load up the board to set the stage
      @test_play = Play.new( game: @test_game, move: "4" , token: @test_game.enemy_token )
      @test_game.apply_move( "0", @test_game.my_token )
      # @test_game.apply_move( "3", @test_game.enemy_token )
      @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.enemy_token )
  
      expect(@test_game.find_best_move).to eq 2
    end
    
    it 'blocks instead of going for a possible win using find_best_move' do
      @test_game = Game.new
      #load up the board to set the stage
      @test_play = Play.new( game: @test_game, move: "4" , token: @test_game.enemy_token )
      @test_game.apply_move( "0", @test_game.my_token )
      # @test_game.apply_move( "3", @test_game.enemy_token )
      @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.enemy_token )
      @test_game.apply_move( "2", @test_game.my_token )
      @test_play = Play.new( game: @test_game, move: "1" , token: @test_game.enemy_token )
  
      expect(@test_game.find_best_move).to eq 7
    end
  
end