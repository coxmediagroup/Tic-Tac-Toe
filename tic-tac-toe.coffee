#!/usr/bin/env coffee
{gets, print, puts, debug, error, inspect, p, log, pump, inherits} = require 'util'
events = require 'events'

# This is an original implementation done without looking at any existing code.
# It follows my practice of making things as simple and as clear as possible
# so that code reviews and maintenance don't have to fight through obscure code.
# I have eschewed "premature" optimization, too. :-)  Heck, I saw an inplementation
# in regex, of all things.

class Board extends events.EventEmitter
    "Create the traditional 3X3 tic-tac-toe board, populated with empty cells."
    constructor: ->
        @blank = "-"
        @board = []
        for i in [0..2]
            @board.push [] # List that represents a row.
            for j in [0..2]
                @board[i][j] = @blank
    contents_of: (position) ->
        @board[ position[0] ][ position[1] ] # Implicit return. CoffeeScript feature.
    mark: (position, player) ->
        @emit "mark error", position unless @contents_of(position) is @blank
        @board[ position[0] ][ position[1] ] = player
        puts "Player #{player} takes #{position}"
    to_string: ->
        "Return a text representation of the board."
        string = ""
        for i in [0..2]
            for j in [0..2]
               string += @board[i][j]
            string += "\n"
        return string
    emit: (signal, argument) ->
        "Just here for debugging so that we can see when events are emitted."
        puts "Emitting signal #{signal} with argument #{argument}" unless signal is "newListener"
        super signal, argument


class Player
    "Simple container for player information."
    constructor: (@me, @board) -> # Put these into instance vars.
        @vectors = new Vectors
        @rules = new Rules @me, @board
        @them = if @me is "X" then "O" else "X" # The VERY funky Coffeescript conditional assignment.
        # puts "I am #{@me}. Opponent is #{@them}."
    move: ->
        for rule in @rules.list
            break if rule(@me, @board) # Stop after a rule makes a move
    manual_move: (position) ->
        @board.mark(position, @me)

class Rules extends events.EventEmitter
    """Just a place to keep the strategy steps that I'm calling rules.
    Methods listed in @list are the strategy steps to take, in proper order.
    The other methods in this class are just helpers."""
    constructor: (@me, @board) -> # Put these into instance vars.
        @blank = "-"
        @them = if @me is "X" then "O" else "X"
        @vectors = new Vectors
        @list = [@win, @block_opponent, @take_center, @take_corner, @take_anything, @board_full] # These are the strategy steps.  Order is critical.
    take_anything: =>
        puts "#{@me} applying rule: take_anything"
        for vector in @vectors.list
            for position in vector
                if @board.contents_of(position) is "-"
                    @board.mark(position, @me)
                    return true
        puts "#{@me} applying rule: take_anything failed to find a blank cell"
        return false # The board is actually full.  We detect that in the next rule."
    board_full: =>
        "No rule could find a move to make.  There are no empty cells."
        @board.emit 'board full'
    win: =>
        puts "#{@me} applying rule: win"
        for vector in @vectors.list
            if @i_can_win_in vector
                # puts "I can win in #{@vector_to_string vector}"
                target = @winning_move_in(vector)
                puts "Winning move: #{target}"
                @board.mark(target, @me)
                @board.emit "wins", @me # Signal to listeners, passing the identity of the winner.
                return true
        puts "  win failed to find a move."
        return false
    block_opponent: =>
        puts "#{@me} applying rule: block"
        for vector in @vectors.list
            # @show_vector(vector)
            if @opponent_can_win_in(vector)
                # puts "Opponent can win in #{@vector_to_string vector}"
                target = @winning_move_in(vector)
                puts "Move to block opponent's win: #{target}"
                @board.mark target, @me
                return true
        puts "  block failed to find a move."
        return false
    take_center: =>
        puts "#{@me} applying rule: take_center"
        position = [1,1]
        if @board.contents_of(position) is "-"
            @board.mark position, @me
            return true
        else
            puts "  take_center failed to find a move."
            return false
    take_corner: =>
        puts "#{@me} applying rule: take_corner"
        for position in [ [0,0], [0,2], [2,0], [2,2] ]
            # puts "pos: #{position}"
            if @board.contents_of(position) is "-"
                @board.mark position, @me
                return true
        puts "take corner failed to find a move."
        return false
    positions_in: (vector, mark) ->
        positions = []
        for position in vector
            #puts "#{position}:  #{board.contents_of(position)}"
            positions.push position if @belongs_to(position, mark)
        return positions
    i_have_one_in: (vector) ->
        return true if @count_in(vector, @me) is 1
    count_in: (vector, mark) ->
        count = 0
        for position in vector
            count += 1 if @board.contents_of(position) is mark
        return count
    i_can_win_in: (vector) ->
        @can_win_in(@me, vector)
    opponent_can_win_in: (vector) ->
        @can_win_in(@them, vector)
    can_win_in: (player, vector) ->
        count = 0
        for position in vector
            count += 1 if @belongs_to(position, player)
            empty_cell = position if @is_blank position
        return true if count is 2 and empty_cell? # We must have two 'owned' cells and one blank.
        return false
    belongs_to: (position, player) ->
        return true if @board.contents_of(position) is player
        return false
    is_mine: (position) ->
        return true if @board.contents_of(position) is @me
        return false
    is_blank: (position) ->
        return true if @board.contents_of(position) is @blank
        return false
    winning_move_in: (vector) ->
        for position in vector
            return position if @board.contents_of(position) is @blank # We have two, this is the position of the blank.
        @emit "winning_move_in error"
    vector_to_string: (vector) =>
        string = ""
        for point in vector
            string += @board.contents_of(point)
        return string
    show_vector: (vector) =>
        puts @vector_to_string(vector)

class Vectors
    "This is the list of all possible ways to win, defined as lists of x/y coordinates."
    constructor: ->
        @list = [
                  # Horizontal.  This is the natural layout and a useful visual map.
                  [ [0,0], [0,1], [0,2] ],
                  [ [1,0], [1,1], [1,2] ],
                  [ [2,0], [2,1], [2,2] ],
                  # Vertical (these rows are actually columns)
                  [ [0,0], [1,0], [2,0] ],
                  [ [0,1], [1,1], [2,1] ],
                  [ [0,2], [1,2], [2,2] ],
                  # Diagonal
                  [ [0,0], [1,1], [2,2] ],
                  [ [2,0], [1,1], [0,2] ]
                ]

