/* global define */
define([
  'underscore',
  'backbone-layout'
], function(_, Layout) {
  'use strict';

  var GameOver = Layout.extend({
    className: 't3-game-over',

    template: _.template(
      '<h3>Game Over</h3>' +
      '<div class="message">Some Message</div>' +
      '<div class="buttons">' +
      '  <button class="btn-new btn-primary-block">Play again</button>' +
      '  <button class="btn-exit btn-primary-block">I give up</button>' +
      '</div>'
    )
  });

  return GameOver;
});

