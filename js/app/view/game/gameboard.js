define(['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    return Backbone.View.extend({
        tagName: 'div',
        id: 'board',

        events : {
            'click .cell': 'onCellClick'
        },
        rendered: false,

        cellHtml: '<div class="cell cell-<%= board %> <%= playerType %>" data-row="<%= row %>" data-column="<%= column %>"></div>',

        template: function() {
            var gameBoard = this.model.get('boardState');
            var html = '';
            _.each(gameBoard, function(boardRow, i) {
                _.each(boardRow, function(cell, j) {
                    html += _.template(this.cellHtml, {
                        board: this.indexToClass(2 * i) + this.indexToClass(2 * j + 1),
                        row: i,
                        column: j,
                        playerType: cell === 0 ? 'none' : cell
                    })
                }, this); //make sure we execute the code in the context of the view.
            }, this);

            return html;
        },

        initialize: function() {
            this.listenTo(this.model, 'change', this.update);
        },

        render: function() {
            if (!this.rendered) {
                this.$el.html(this.template());
                this.rendered = true;
            }
            return this;
        },

        update: function() {
            var gameBoard = this.model.get('boardState');
            _.each(gameBoard, function(boardRow, i) {
                _.each(boardRow, function(cell, j) {
                    var cellCls = '.cell-' + this.indexToClass(2*i) + this.indexToClass(2* j + 1);
                    if (gameBoard[i][j] !== 0) {
                        $(cellCls).addClass(gameBoard[i][j]).removeClass('none');
                    }
                }, this); //make sure we execute the code in the context of the view.
            }, this);
        },

        indexToClass:  function(index) {
            var cssClass = '';
            switch (index) {
                case 0:
                    cssClass = 't';
                    break;
                case 1:
                    cssClass = 'l';
                    break;
                case 2:
                case 3:
                    cssClass = 'm';
                    break;
                case 4:
                    cssClass = 'b';
                    break;
                case 5:
                    cssClass = 'r';
            }

            return cssClass;
        },

        onCellClick: function(cell) {
            if (this.model.get('player').get('isCurrent')) {
                var boardState = this.model.get('boardState');
                var row = parseInt(cell.target.dataset.row);
                var col = parseInt(cell.target.dataset.column);

                if (boardState[row][col] === 0) {
                    boardState[row][col] = this.model.get('player').get('playerType');
                    this.model.unset('boardState', { silent : true });
                    this.model.set('boardState', boardState);
                }
            }
        }
    });
});