/* global define */
define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  'use strict';

  var Board = Backbone.Collection.extend({
    initialize: function() {
      this.add([
        { owner: null }, // ignore index 0
        { owner: null }, { owner: null }, { owner: null },
        { owner: null }, { owner: null }, { owner: null },
        { owner: null }, { owner: null }, { owner: null }
      ]);
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

