require_relative '../classes/play'
require_relative '../classes/game'
require 'yaml'
require 'spec_helper'

RSpec.describe Play do
  
  it 'finds the right slot to fill for a win' do
    @test_game = Game.new
    #load up the board to set the stage
    @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.enemy_token )
    @test_game.apply_move( "0", @test_game.my_token )
    @test_game.apply_move( "1", @test_game.my_token )  
    
    expect(@test_play.find_best_move).to eq 2
   end
   
   it 'finds the right slot to fill to block a threat' do
     @test_game = Game.new
     #load up the board to set the stage
     @test_play = Play.new( game: @test_game, move: "8" , token: @test_game.my_token )
     @test_game.apply_move( "2", @test_game.enemy_token )
     @test_game.apply_move( "6", @test_game.enemy_token )
    
     expect(@test_play.find_best_move).to eq 4
    end
end