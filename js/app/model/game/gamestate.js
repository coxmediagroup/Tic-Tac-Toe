define(['jquery', 'underscore', 'backbone', 'model/player/player', 'model/player/npcplayer'],
    function($, _, Backbone, Player, NPCPlayer) {
     return Backbone.Model.extend({

         initialize: function() {
            this.set('player', new Player({
                playerType: 'PC',
                isCurrent: true
            }));
            this.set('computer', new NPCPlayer);
            this.set('currentPlayer', this.get('player'));
            this.set('boardState',  [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]);
         },

         hasWinningRow: function() {
             var board = this.get('boardState');

             for (var i = 0; i < 3; i++) {
                 var colAlike = 0;
                 var lastCol = 0;
                 for (var j = 0; j < 3; ++j) {
                     if (board[i][j] !== 0) {
                         if (board[i][j] === lastCol) {
                             colAlike++;
                         } else {
                             lastCol = board[i][j];
                         }
                     }
                 }

                 if (colAlike === 3) {
                     return true;
                 }
             }

             return false;
         },

         hasWinningColumn: function() {
             var board = this.get('boardState');

             for (var i = 0; i < 3; ++i) {
                 var colAlike = 0;
                 var lastCol = 0;
                 for (var j = 0; j < 3; ++j) {
                     if (board[j][i] !== 0) {
                         if (board[j][i] === lastCol) {
                             colAlike++;
                         } else {
                             lastCol = board[j][i];
                         }
                     }
                 }

                 if (colAlike === 3) {
                     return true;
                 }
             }

             return false;
         },

         hasWinningDiagonal: function() {
             var board = this.get('boardState');
             var colAlike = 0;

             for (var j = 0; j < 3; ++j) {
                 var lastCol = 0;
                 if (board[j][j] !== 0) {
                     if (board[j][j] === lastCol) {
                         colAlike++;
                     } else {
                         lastCol = board[j][j];
                     }
                 }
             }

             if (colAlike === 3) {
                 return true;
             }

             colAlike = 0;

             for (var i = 2, k = 0; i >= 0; --i, k++) {
                 var lastCol = 0;
                 if (board[i][k] !== 0) {
                     if (board[i][k] === lastCol) {
                         colAlike++;
                     } else {
                         lastCol = board[i][k];
                     }
                 }
             }

             return colAlike === 3;
         },

         isGameOver: function() {
             if (this.allMovesMade()) {
                return true;
             } else if (this.hasWinningRow() || this.hasWinningColumn() || this.hasWinningDiagonal()) {
                return true;
             } else {
                 return false;
             }
         },

         allMovesMade: function() {
             var board = this.get('boardState');

             for (var i = 0; i < 3; i++) {
                 for (var j = 0; j < 3; ++j) {
                     if (board[i][j] === 0) {
                        return false;
                     }
                 }
             }

             return true;
         },

         sync: function(method, model, options) {

         }
     });
});