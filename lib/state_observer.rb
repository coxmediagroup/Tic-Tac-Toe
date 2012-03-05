#
#  class:         StateObserver
#  extends:       --
#  module:        TicTacToe
#  author:        Joseph Weissman, <jweissman1986@gmail.com>
#
module TicTacToe
 
  #
  #   Observes the current state of the game and provides some rendering and endgame
  #   detection facilities; in charge of most of the logic around inspection and analysis of
  #   board configuration.
  #
  class StateObserver

    #
    #  Determine whether the state is terminal.
    #
    def terminal?(state)
      filled?(state) or win_condition_achieved?(state)
    end

    #
    #   determine whether the board is filled.
    #
    def filled?(state)
      not state.board.include? 0
    end

    #
    #   Determine whether the game was won.
    #
    def win_condition_achieved?(state)
      winner(state) != 0
    end


    #
    #   determine who the winner of the current state is (returns 0 if cannot
    #   be determined yet/draw)
    #
    def winner(state)
      win_player = 0
      each_line(state) do |line|
        if line.first != 0 and line.uniq.length == 1
          # the player with that mark has won
          win_player = line.first
          break
        end
      end

      win_player
    end


    #
    #   Assemble an array containing the rows, columns and diagonal elements
    #   of the state.
    #
    def each_line(state)
      m = matrix(state)

      lines = (m + m.transpose +

      # diagonals
      [ (0..2).collect { |i| m[i][i] },
        (0..2).collect { |i| m[i][2-i] } ] )

      lines.each do |line|
        yield line
      end
    end


    #
    #   Assemble a 2-d array with the elements of the board.
    #
    def matrix(state)
      f = state.board
      [[f[0], f[1], f[2]],
       [f[3], f[4], f[5]],
       [f[6], f[7], f[8]]]
    end

    

    #
    #  Determine whether the game is a draw.
    #
    def draw?(state)
      filled?(state) and winner(state) == 0
    end


    #
    #  determine whether the winner of the state is the player with provided index
    #
    def player_won?(state, player)
      winner(state) == player
    end

    #
    #   Assembles an array of available positions/moves for the given state.
    #
    def open_positions(state)
      open = []
      state.board.each_with_index { |c, i| open << i if c == 0 }
      open
    end

    #
    #   Iterator over immediate successor states of the provided state.
    #
    def each_immediate_successor_state(state)
      raise StandardError.new("no successors; game is over") if terminal? state
      open_positions(state).each { |position| yield state.successor(position) }
    end

    #
    #  Iterator over immediate successor states, constructing them if need be
    #  (combination of previous two methods). Note the return value is an
    #  array with two elements: the successor state resulting
    #  from the current player moving a given position and the index of that
    #  position in the board array.
    #
    def each_immediate_successor_state_with_index(state)
      open_positions(state).each { |n| yield [state.successor(n), n] }
    end





    #
    #  Perform a simple evaluation of the state under observation for the given
    #  player, namely:
    #
    #     state           value returned by StateObserver.evaluate(state,player)
    #     -----           ------------------------------------------------------
    #
    #     draw                                     0
    #     win                                     +1
    #     loss                                    -1
    #
    #
    def evaluate(state, player=1)
      return 0 if draw?(state)
      player_won?(state, player) ? 1 : -1
    end


    #
    #    Return a human-friendly string expressing the state's
    #    current status -- in progress, drawn, or won by a particular player.
    #
    def disposition(state)
      raise ArgumentError.new("state cannot be nil") if state.nil?
      return "game is in-progress" if not terminal? state
      if player_won?(state, 1)
        return "player one is victorious"
      elsif player_won?(state, 2)
        return "player two is victorious"
      else
        return "game ended in a draw"
      end
    end

    #
    #     Format and display the schematic representation of the state.
    #
    def pp(state,value_map=[' ','X','O'])
      puts pretty(state,value_map)
    end

    #
    #    Format a schematic representation of a game state.
    #
    def pretty(state,value_map=[' ','X','O'])
      txt = StringIO.new

      m = matrix(state)
      m.each_with_index do |row, n|
        txt << row.map do |value|
          mark = value_map[value]
          line = " #{mark} "
          line
        end.join('|') << "\n"

        # draw a line between each row
        txt << "-"*((3*3)+(2)) << "\n" unless n == 2
      end

      txt.rewind
      txt.read
    end
  end # end class StateObserver
end # end module TicTacToe