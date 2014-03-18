/* global define */
define([
  'backbone',
  'underscore',
  'backbone-layout'
], function(Backbone, _, Layout) {
  'use strict';

  // CollectionView
  // --------------

  // The `CollectionView` view should be used as a container view for a
  // collection of sub views that are built against a collection of models.
  //
  // As a concrete example: a `CollectionView` would be a good view for a list
  // of Todo models where the `CollectionView` itself would define the overall
  // structure for the list of views (and manage them).
  var CollectionView = Layout.extend({

    // ##tagName
    // By default the tag will be `<ul>`. This can be overridden by
    // subclasses.
    tagName: 'ul',

    // ##initialize
    initialize: function(options) {
      options || (options = {});
      Layout.prototype.initialize.call(this, options);

      // If `ElementView` is defined in the options, use it.
      options.ElementView && (this.ElementView = options.ElementView);
    },

    // ##defaults
    //
    // By default all `CollectionView` objects will contain a reference to a
    // `Backbone.Collection` instance.
    defaults: {
      'collection': new (Backbone.Collection.extend())()
    },

    // ##createView
    //
    // Create the `ElementView` of this model. Delegates the view arguments to
    // the `getViewArgs` method.
    //
    // This method is commonly overridden by sub classes when custom work
    // needs to be done before or after the `ElementView` is created (or if
    // the view needs to be created in some special way).
    createView: function(model) {
      return new this.ElementView(this.getViewArgs(model));
    },

    // ##getViewArgs
    //
    // Return the arguments that will be passed to an `ElementView`
    // constructor for the given model.
    //
    // This method is commonly overridden in order to provide customized
    // arguments to `ElementView` instances as they are created by the
    // `createView` method.
    getViewArgs: function(model) {
      return {model: model};
    },

    // ##addOne
    //
    // Append a new `ElementView` instance to the `views` collection and then
    // render it at the end of the list of views.
    addOne: function(model) {
      var view = this.createView(model);
      this.registerView(view);
      this.renderElement(view);
      this.trigger('addone', model, view, this);
      return view;
    },

    // ##renderElement
    //
    // Render a view element. By default the view is just added to the end of
    // the parent DOM element, but this can be overridden.
    renderElement: function(view) {
      this.$el.append(view.render().el);
    },

    // ##addAll
    //
    // Empty the list (and DOM elements) and re-render the collection.
    addAll: function() {

      // Unregister (remove)
      this.viewManager.each(function(mView) {
        var view = mView.view;
        this.unRegisterView(view);
        view.trigger('remove', view, this);
      }, this);

      // Add everything
      _(this.getModels()).each(function(model) {
        this.addOne(model);
      }, this);
    },

    // ##getModels
    //
    // Return the associated models. By default this just returns the list of
    // models stored in `this.collection`.
    getModels: function() {
      return this.collection.models;
    },

    // ##getViewElements
    //
    // Return the DOM elements associated with the views.
    getViewElements: function() {
      return _.map(this.viewManager.getViews(), function(view) {
        return view.$el;
      });
    },

    // ##fetch
    //
    // Call `fetch` on `this.collection`
    fetch: function(options) {
      this.collection.fetch(options);
    }
  });

  return CollectionView;
});








