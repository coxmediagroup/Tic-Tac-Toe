require.config({
  baseUrl: "static/js/libs",
  paths: {
    jquery: "jquery/jquery",
    underscore: "underscore/underscore",
    app: "../app"
  }
});

require([
  'app',
], function(TicTacToe) {
  'use strict';

  var tictactoe = new TicTacToe();

  tictactoe.initialize();

  window.tictactoe = tictactoe;

});

