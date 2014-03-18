/* global define */
define([
  'underscore',
  'backbone-layout',
  'views/collection',
  'apps/tic-tac-toe/board'
], function(_, Layout, CollectionView, Board) {
  'use strict';

  var CellView = Layout.extend({
    className: 't3-col-view',

    events: {
      'click': 'handleClick'
    },

    template: _.template(
      '<%= mark %>'
    ),

    handleClick: function() {
      this.trigger('clicked', this);
    },

    initialize: function() {
      this.listenTo(this.model, 'change:owner', this.render);
    },

    serialize: function() {
      var mark = '';
      if (this.model.get('owner')) {
        mark = this.model.get('owner').get('mark');
      }
      return { mark: mark };
    }
  });

  var Game = CollectionView.extend({
    tagName: 'div',

    className: 'game-view',

    ElementView: CellView,

    template: _.template(
      '<div class="game">' +
        '<div class="t3-row row-1">' +
        '  <div data-val="8" class="t3-col"></div>' +
        '  <div data-val="1" class="t3-col"></div>' +
        '  <div data-val="6" class="t3-col"></div>' +
        '</div>' +
        '<div class="t3-row row-2">' +
        '  <div data-val="3" class="t3-col"></div>' +
        '  <div data-val="5" class="t3-col"></div>' +
        '  <div data-val="7" class="t3-col"></div>' +
        '</div>' +
        '<div class="t3-row row-3">' +
        '  <div data-val="4" class="t3-col"></div>' +
        '  <div data-val="9" class="t3-col"></div>' +
        '  <div data-val="2" class="t3-col"></div>' +
        '</div>' +
      '</div>'
    ),

    initialize: function(options) {
      Layout.prototype.initialize.call(this, options);

      // Store reference to the state object
      this.state = this.options.state;
      this.players = this.options.players;

      this.collection = new Board();

      this.listenTo(this.collection, 'change:owner', this.handleChangeOwner);

      // Bind to the `CellView`'s bubbled up click event
      this.on('clicked', function(cellView) {
        if (_.isNull(cellView.model.get('owner'))) {
          cellView.model.set('owner', this.state.get('player'));
        }
      }, this);
    },

    // ##getBoard
    // External getter for the collection object.
    getBoard: function() {
      return this.collection;
    },

    handleChangeOwner: function() {
      var args = _.union('change:owner', arguments);
      this.trigger.apply(this, args);
    },

    afterRender: function() {
      this.addAll();
    },

    renderElement: function(view) {
      var index = _.indexOf(this.viewManager.getViews(), view);
      if (index === 0) {return;}
      $('[data-val=' + index + ']', this.el).html(view.render().el);
    },

    getWinFor: function(pairs) {
      return this.collection.getWinFor(pairs);
    },

    findForkFor: function(player) {
      return this.collection.findForkFor(player);
    },

    getCornerOpposite: function(player) {
      return this.collection.getCornerOpposite(player);
    },

    getEmptyCorner: function() {
      return this.collection.getEmptyCorner();
    },

    getEmptySide: function() {
      return this.collection.getEmptySide();
    },

    findBlockForFork: function(cell, player) {
      return this.collection.findBlockForFork(cell, player);
    },

    findWinningCells: function() {
      return this.collection.findWinningCells();
    },

    reset: function() {
      this.collection.each(function(cell) {
        cell.set('owner', null);
      });
    }
  });

  return Game;
});
