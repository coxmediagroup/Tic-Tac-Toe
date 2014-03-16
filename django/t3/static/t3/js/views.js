/* global define */
define([
  'views/title-screen'
], function(TitleScreen) {
  'use strict';

  // Views
  // -----

  // Simply a requirejs module that allows modularization of all the `T3`
  // views for easy packaging and reference later.
  var Views = {
    TitleScreen: TitleScreen
  };

  return Views;
});
