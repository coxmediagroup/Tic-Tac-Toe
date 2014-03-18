/* global define */
define([
  'apps/tic-tac-toe/app'
], function(App) {
  'use strict';

  // TicTacToe
  // ---------

  // Just like the other module packages, this just collects the various pieces
  // of the TicTacToe application together.
  //
  // While I didn't do it here, it would usually make sense to also include any
  // other meta information about the TicTacToe game (versions, etc) at this
  // level.
  var TicTacToe = {
    App: App
  };

  return TicTacToe;
});
