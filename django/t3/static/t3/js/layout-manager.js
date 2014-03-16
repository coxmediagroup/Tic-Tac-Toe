/* global define */
define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  'use strict';

  // Use backbone's copy of jQuery
  var $ = Backbone.$;

  // LayoutManager
  // -------------

  // The layout manager's job is to manage a particular section of the DOM and
  // attach/detach Layout views to/from that element.
  //
  // It is also responsible for ensuring that any previously shown view is
  // appropriately closed before the new view is shown. This helps prevent
  // zombie binds from occurring.
  //
  // This is a class I use in almost every Backbone project (usually in
  // conjunction with `backbone-layout`). I would have just included this as a
  // bower dependency but currently my github project for this class is out of
  // date.
  var LayoutManager = function(options) {
    options || (options = {});
    this.anchor = options.anchor || '#content';
    this.context = options.context || null;
  };

  var defaults = {
    // Before the view is rendered
    beforeRender: function() {},

    // After the view is rendered
    afterRender: function() {},

    // Before the view is attached to the DOM (but after it is rendered)
    beforeShow: function() {},

    // After the view is attached to the DOM
    afterShow: function() {},

    // If the view is not shown (it was already being shown)
    onNoShow: function() {},

    // The very first operation
    first: function() {},

    // The very last operation
    last: function() {},

    // Force the view to show even if it is already shown.
    force: false,

    // Don't actually render the view.
    doRender: true
  };

  _.extend(LayoutManager.prototype, Backbone.Events, {

    // ##showView
    // Shows a specific `Backbone.View` (generally a `Layout`).
    // The `defaults` above can be overridden via the `options` parameter.
    showView: function(view, options) {
      options || (options = {});
      options = _.defaults(options, defaults);

      options.first();

      // This is the heart of the layout manager.
      //
      // Render and display the view. Checks are done to make sure that the
      // view should be shown/rendered.
      if (this.currentView !== view || (options && options.force)) {
        this.currentView && this.currentView.close();
        this.currentView = view;

        options.beforeRender();
        options.doRender && this.currentView.render();
        options.afterRender();

        options.beforeShow();
        $(this.anchor, this.context).empty().append(this.currentView.el);
        options.afterShow();
      } else {
        options.onNoShow();
      }
      options.last();
    }
  });

  return LayoutManager;
});
