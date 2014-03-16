/* global define */
define(['underscore', 'backbone-layout'], function(_, Layout) {
  'use strict';

  // TitleScreen
  // -----------

  // The title screen of the application.
  var TitleScreen = Layout.extend({
    className: 'title-screen',

    events: {
      'click .btn-yes': 'handleYes'
    },

    template: _.template(
      '<img class="banner" src="static/t3/img/wargames.jpg" />' +
      '<div class="buttons">' +
      '  <button class="btn-yes btn-primary-block" type="button">Yes</button>' +
      '</div>'
    ),

    handleYes: function() {
      this.options.state.set('name', 't3:startup');
    }
  });

  return TitleScreen;
});
