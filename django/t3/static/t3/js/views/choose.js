/* global define */
define([
  'underscore',
  'backbone-layout'
], function(_, Layout) {
  'use strict';

  var Choose = Layout.extend({
    className: 'game-startup',

    template: _.template(
      '<h3>How about a nice game of chess?</h3>' +
      '<div class="alert alert-danger" style="display:none"></div>' +
      '<div class="buttons">' +
      '  <button data-opt="chess" class="btn-chess btn-primary-block">Play: Chess</button>' +
      '  <button data-opt="gtnw" class="btn-gtnw btn-primary-block">Play: Global Thermonuclear War</button>' +
      '  <button data-opt="t3" class="btn-t3 btn-primary-block">Play: Tic-Tac-Toe</button>' +
      '</div>'
    ),

    events: {
      'click button': 'handleButtonClick'
    },

    handleButtonClick: function(event) {
      this.trigger('play', $(event.target).data('opt'), this);
    }
  });

  return Choose;
});
