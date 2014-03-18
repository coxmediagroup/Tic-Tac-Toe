/* global define */
define([
  'underscore',
  'backbone-layout',
], function(_, Layout) {
  'use strict';

  var Footer = Layout.extend({
    className: 'game-footer',

    template: _.template(
      '<div class="footer">' +
      '  <div class="game-player">' +
      '    <label>Player:</label>' +
      '    <span class="value"><%= player %></span>' +
      '  </div>' +
      '  <div class="game-move">' +
      '    <label>Move:</label>' +
      '    <span class="value"><%= move %></span>' +
      '  </div>' +
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      this.listenTo(this.model, 'change:player', this.render);
      this.listenTo(this.model, 'change:move', this.render);
    },

    serialize: function() {
      var player = this.model.get('player');
      return {
        player: player ? player.get('name') : '',
        move: this.model.get('move') + 1
      };
    }
  });

  return Footer;
});
