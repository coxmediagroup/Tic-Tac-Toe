/* global define */
define([
  'views/choose',
  'views/title-screen'
], function(Choose, TitleScreen) {
  'use strict';

  // Views
  // -----

  // Simply a requirejs module that allows modularization of all the `T3`
  // views for easy packaging and reference later.
  var Views = {
    Choose: Choose,
    TitleScreen: TitleScreen
  };

  return Views;
});
