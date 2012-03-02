require 'stringio'

require 'game'
require 'board'
require 'player'

require 'human_player'
require 'computer_player'
require 'maximizing_player'

module TicTacToe

    VERSION = '0.0.1'
    AUTHOR  = 'Joseph Weissman <jweissman1986@gmail.com>'

    def self.banner; "TicTacToe v#{VERSION}. Written by #{AUTHOR}, 2012."; end

end