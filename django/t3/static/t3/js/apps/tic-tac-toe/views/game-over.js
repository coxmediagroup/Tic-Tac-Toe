/* global define */
define([
  'underscore',
  'backbone-layout'
], function(_, Layout) {
  'use strict';

  var GameOver = Layout.extend({
    className: 't3-game-over',

    events: {
      'click .btn-new': 'handleNewGameClick',
      'click .btn-exit': 'handleExitGameClick'
    },

    template: _.template(
      '<h3>Game Over</h3>' +
      '<div class="message"><%= message %></div>' +
      '<div class="buttons">' +
      '  <button class="btn-new btn-primary-block">Play again</button>' +
      '  <button class="btn-exit btn-primary-block">I give up</button>' +
      '</div>'
    ),

    handleNewGameClick: function() {
      this.trigger.apply(this, _.union(['clicked-new'], arguments));
    },

    handleExitGameClick: function() {
      this.trigger.apply(this, _.union(['clicked-exit'], arguments));
    },

    serialize: function() {
      return this.options;
    }
  });

  return GameOver;
});

