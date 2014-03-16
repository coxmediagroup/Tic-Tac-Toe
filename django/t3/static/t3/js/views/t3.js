/* global define */
define([
  'backbone-layout'
], function(Layout) {
  'use strict';

  var TicTacToe = Layout.extend({
    className: 't3-game'
  });

  return TicTacToe;
});
