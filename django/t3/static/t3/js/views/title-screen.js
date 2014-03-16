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

    handleYes: function(event) {
      // Bubble the event up. Let the application handle it.
      this.trigger('click:yes', event, this);
    }
  });

  return TitleScreen;
});
