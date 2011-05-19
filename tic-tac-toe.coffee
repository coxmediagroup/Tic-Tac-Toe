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
        # puts "Emitting signal #{signal} with argument #{argument}" unless signal is "newListener"
        super signal, argument
