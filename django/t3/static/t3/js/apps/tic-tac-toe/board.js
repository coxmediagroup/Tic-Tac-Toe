/* global define */
define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  'use strict';

  // To make checking for wins a little faster, just store the valid winning
  // cell combinations as a constant.
  var WINNING_COMBOS = [
    // Rows       Cols      Diags
    [8, 1, 6], [8, 3, 4], [8, 5, 2],
    [3, 5, 7], [1, 5, 9], [6, 5, 4],
    [4, 9, 2], [6, 7, 2]
  ];

  var Board = Backbone.Collection.extend({
    initialize: function() {
      this.add([
        { owner: null }, // ignore index 0
        { owner: null }, { owner: null }, { owner: null },
        { owner: null }, { owner: null }, { owner: null },
        { owner: null }, { owner: null }, { owner: null }
      ]);
    },

    // ##findWinningCells
    // Returns the specific cells that constitute a winning combo
    findWinningCells: function() {
      var winning = [];
      _.each(WINNING_COMBOS, function(cellIds) {
        var cells = _.map(cellIds, function(num) {
          return this.at(num);
        }, this);
        var byPlayer = _.countBy(cells, function(cell) {
          var owner = cell.get('owner');
          return owner ? owner.get('name') : '';
        });
        if (byPlayer.computer === 3 || byPlayer.human === 3) {
          winning = cells;
        }
      }, this);
      return winning;
    },

    findWinsFor: function(pairs) {
      var wins = this.filter(function(cell, index) {
        if (index === 0) { return ;}
        if (!cell.get('owner')) {
          if (pairs[15 - index]) {
            return cell;
          }
        }
      });
      return wins;
    },

    getWinFor: function(pairs) {
      var wins = this.findWinsFor(pairs);
      if (wins.length) { return wins[0]; }
      return null;
    },

    findForkFor: function(player) {
      var forks = this.filter(function(cell, index) {
        if (index === 0 || cell.get('owner')) { return; }

        // Clone this to preserve the pairs/taken arrays.
        var clone = player.deepClone();

        // Check if after taking this cell the human would have a winning move
        clone.updatePairs(index);
        var wins = this.findWinsFor(clone.pairs);

        // If there is just one win, don't bother with it since the algorithm
        // already knows how to handle blocking a single winning cell.
        if (wins && wins.length >= 2) {
          return true;
        }
        return false;
      }, this);
      if (forks.length) { return forks[0]; }
      return null;
    },

    // ##findBlockForFork
    // Run a test that assumes the forkCell has been taken by player and then
    // find a subsequent winning move.
    findBlockForFork: function(forkCell, player) {
      var clone = player.deepClone();
      var index = this.indexOf(forkCell);
      clone.updatePairs(index);
      return this.getWinFor(clone.pairs);
    },

    getCornerOpposite: function(player) {
      var ownedCorners = this.filter(function(cell, index) {
        if (index === 0) { return false; }

        // All the corner cells are even
        var isCorner = !(function() {
          return index % 2;
        })();

        return isCorner && cell.get('owner') === player;
      }, this);

      var opposites = [];
      _.each(ownedCorners, function(corner) {
        var idx = this.indexOf(corner);

        // The corners always add up to 10, so its very easy to find the
        // opposite corner if the first corner's index is known.
        if (_.isNull(this.at(10 - idx).get('owner'))) {
          opposites.push(this.at(10 - idx));
        }
      }, this);

      if (opposites.length) { return opposites[0]; }
      return null;
    },

    getEmptyCorner: function() {
      var empty = this.filter(function(cell, index) {
        if (index === 0) { return; }
        var isCorner = !(function() {
          return index % 2;
        })();
        return isCorner && _.isNull(cell.get('owner'));
      }, this);
      if (empty.length) { return empty[0]; }
      return null;
    },

    getEmptySide: function() {
      var empty = this.filter(function(cell, index) {
        if (index === 0) { return; }
        var isSide = (function() {
          return index % 2;
        })();
        return isSide && _.isNull(cell.get('owner'));
      }, this);
      if (empty.length) { return empty[0]; }
      return null;
    }
  });

  return Board;
});

