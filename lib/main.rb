=begin

  main.rb


  Application entrypoint -- launches a game playable via console.

  (Should make this parameterized with command-line arguments?)


=end

require 'tic_tac_toe'


puts TicTacToe::banner
TicTacToe::Game.new(:size => [3,3], :humans => 1).play!