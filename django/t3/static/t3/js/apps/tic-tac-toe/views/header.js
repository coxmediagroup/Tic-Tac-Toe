/* global define */
define([
  'underscore',
  'backbone-layout',
], function(_, Layout) {
  'use strict';

  var Header = Layout.extend({
    className: 'game-header',

    template: _.template(
      '<div class="header">' +
      '  <div class="games-played">' +
      '    <label>Played:</label>' +
      '    <span class="value"><%= gamesPlayed %></span>' +
      '  </div>' +
      '  <div class="games-won">' +
      '    <label>Won:</label>' +
      '    <span class="value"><%= gamesWon %></span>' +
      '  </div>' +
      '  <div class="games-lost">' +
      '    <label>Lost:</label>' +
      '    <span class="value"><%= gamesLost %></span>' +
      '  </div>' +
      '  <div class="games-tied">' +
      '    <label>Tied:</label>' +
      '    <span class="value"><%= gamesTied %></span>' +
      '  </div>' +
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);
      this.listenTo(this.model, 'change', this.render);
    }
  });

  return Header;
});
