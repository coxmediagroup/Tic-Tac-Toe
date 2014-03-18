/* global define */
define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  'use strict';

  // AppBase
  // -------

  // The application base class for any Application type class.
  // If this were a larger project then this would define some common interface
  // methods and would do some clever binding to a dedicated Router. As it
  // stands, all I need from the application instance is for it to be able to
  // trigger events.
  var AppBase = function(options) {
    options || (options = {});
    this.options = options;

    this.initialize && this.initialize(options);
  };

  // Make this extenstible
  AppBase.extend = Backbone.Model.extend;

  // Extend with Backbone.Events
  _.extend(AppBase.prototype, Backbone.Events);

  return AppBase;
});
