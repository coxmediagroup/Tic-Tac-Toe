/* global define */
define([
  'apps/tic-tac-toe'
], function(TicTacToe) {
  'use strict';

  // Apps
  // ----

  // Aggregate the applications into one module for ease of use and better
  // minification later.
  var Apps = {
    TicTacToe: TicTacToe
  };

  return Apps;
});
