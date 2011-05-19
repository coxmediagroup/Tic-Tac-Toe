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
        @list = [@win, @block_opponent,] # These are the strategy steps.  Order is critical.
