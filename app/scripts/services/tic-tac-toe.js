/*global $:false */
'use strict';

angular.module('TicTacToeApp')
.factory('TicTacToeBoard', [function() {
  
  var x = 'X';
  var o = 'O';
  
  var board = {
    length: 3,
    width: 3,
    
    // public, use in ng-bind
    board: [],
    
    // private sets to check for win conditions
    occupy: {
      o: { player: o, set: []},
      x: { player: x, set: []}
    },
    lastMove: undefined,
    
    /**
     * creates an empty block to be placed on the board.
     */
    createEmpty: function() {
      return { txt: 'EMPTY', cls: 'empty', player: undefined};
    },
    
    /**
     * creates an O-player block to be placed on the board.
     */
    createO: function() {
      return { txt: 'O', cls: 'o', player: o};
    },
    
    /**
     * creates an X-player block to be placed on the board.
     */
    createX: function() {
      return { txt: 'X', cls: 'x', player: x};
    },
    
    /**
     * Initialize the board to the start point.
     * (safe to call for reinitialization).
     */
    init: function() {
      this.board = [];
      for(var i=0;i<(this.length * this.width);i++) {
        this.board.push(this.createEmpty());
      }
      this._player = o;
      this.lastMove = undefined;
      
      // ai player plays first.
      this.aiMove();
    },
    
    /**
     * Switches active player.
     */
    togglePlayer: function() {
      this._player = (this._player === x) ? o : x;
    },
    
    /**
     * Selects a spot on the board for block insertion.
     * Uses the internally tracked active player.
     * 
     * Returns - true if move was successful, false otherwise.
     */
    select: function(block) {
      
      var idx = this.board.indexOf(block);
      
      // don't allow a move on occupied space or further moves
      // after a win.
      if(this.board[idx].player !== undefined || this.checkForWin()){ return false; }
      this.lastMove = idx;
      
      var peice;
      
      if(this._player === x) {
        peice = this.createX();
        this.occupy.x.set.push(idx);
      } else {
        peice = this.createO();
        this.occupy.o.set.push(idx);
      }
      
      this.board[idx] = peice;
      this.togglePlayer();
      return true;
    },
    
    /**
     * Takes the last move made into account
     * and then takes a defensive move to prevent
     * user from winning.
     */
    aiMove: function() {
      
      var self = this;
      
      if(self.lastMove === undefined) {
        self.select(self.board[4]);
        return;
      }
      
      var nextMoves = {
        0: [1, 3],
        1: [2, 0, 4],
        2: [1, 5],
        3: [4, 0, 6],
        4: [5, 3, 1, 7],
        5: [4, 2, 8],
        6: [7, 3],
        7: [8, 4, 6],
        8: [5, 7]
      };
      
      var moved = false;
      $.each(nextMoves[self.lastMove], function(idx, val) {
        if(!moved && self.board[val].player === undefined) {
          self.select(self.board[val]);
          moved = true;
          return;
        }
      });
      
      if(!moved) {
        $.each(self.board, function(idx, val) {
          if( !moved && val.player === undefined) {
            self.select(val);
            moved = true;
            return;
          }
        });
      }
    },
    
    /**
     * Looks at the tic-tac-toe board for
     * an active win condition being met returns
     * either undefined (no win) or the player that
     * has won.
     */
    checkForWin: function() {
      
      var wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
      ];
      
      var win = false;
      
      var self = this;
      $.each(self.occupy, function(idx, p) {
        $.each(wins, function(idx, w) {
          
          var stop = false;
          $.each(w, function(idx, e) {
            if( p.set.indexOf(e)< 0 || stop ) { stop = true; return; }
            if(idx === 2){ win = p; }
          });
        });
      });
      return win;
    },
    
    /**
     * resets the board to the base state and
     * re-initializes it.
     */
    resetBoard: function() {
      $.each(this.occupy, function(idx, p) {
        p.set = [];
      });
      this.init();
    }
  };
  
  // init on module load.
  board.init();
  return board;
}]);
