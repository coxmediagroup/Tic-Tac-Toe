/* global define */
define([
  'views/title-screen',
  'views/t3'
], function(TitleScreen, T3) {
  'use strict';

  // Views
  // -----

  // Simply a requirejs module that allows modularization of all the `T3`
  // views for easy packaging and reference later.
  var Views = {
    TitleScreen: TitleScreen,
    T3: T3
  };

  return Views;
});
