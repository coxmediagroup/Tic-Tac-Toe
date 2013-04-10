// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){
  // Game Model

  var Game = Backbone.Model.extend({

    defaults: function() {
      return {
        GameName: "New Game",
        order: Games.nextOrder(),
        isActive: false,
        isEditingName: false,
        important: false,
        navTab: "all_tab",
        allMoves: [false,false,false,false,false,false,false,false,false]
      };
    },

    initialize: function() {
      if ( !this.get("GameName") ) 
           this.set({"GameName": this.defaults().GameName});

      if ( !this.get("allMoves") ) 
           this.set({"allMoves": this.defaults().allMoves});
    
     },

    toggleActive: function() {
      this.save({isActive: !this.get("isActive")});  },

    toggleImportant: function() {
      this.save({important: !this.get("important")});  },

    setEditingName: function() {
      this.save({isEditingName: true}); },

	allmoves_save: function(ar){
		this.save({allMoves: ar});

},


  });


  

  // Game Collection
  // ---------------

  // The collection of characters is backed by *localStorage* instead of a remote server.
  var GameList = Backbone.Collection.extend({
    // Reference to this collection's model.
    model: Game,
    // Save all of the Game items under the `Game-backbone` namespace.
    localStorage: new Backbone.LocalStorage("Game-backbone"),
    // Filter down the list of all Character items that are alive.
    isActive: function() {
      return this.filter(function(Game){ return Game.get('isActive'); });
    },

    isImportant: function() {
      return this.filter(function(Game){ return Game.get('important'); });
    },
    // Filter down the list to only todo items that are still not finished.
    remaining: function() {
      return this.without.apply(this, this.isActive());
    },

    isEditingName: function() {
      return this.filter(function(Game){ return Game.get('isEditingName'); });
    },

    // We keep the Games in sequential order, despite being saved by unordered
    // GUID in the database. This generates the next order number for new items.
    nextOrder: function() {
      if (!this.length) return 1;
      return this.last().get('order') + 1;
    },

      // Games are sorted by their original insertion order.
    comparator: function(Game) {
      return Game.get('order');
    }




  });

  // Create our global collection of **Games**.
  var Games = new GameList;
  var GameView = Backbone.View.extend({
    tagName:  "li",
    // Cache the template function for a single item.
    template: _.template($('#Game-tree-template').html()),

    // The DOM events specific to an item.
    events: {
      "dblclick .view"  : "edit",
      "click .toggle"   : "toggleIsActive",
      "keypress .edit"  : "updateOnEnter",
      "blur .edit"      : "close",
      "click .important"   : "toggleImportant"
    },

    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
  
    // Re-render the Game management tree
    render: function() {
       if ( this.model.get("navTab") == "lost_tab" && !this.model.get("important") )
         {  // Remove all Games from the list which are not marked (Important tab)
           this.$('.view').remove();
           this.$('.important').remove();
           this.$el.toggleClass('highlight', false) 
         }
      else { // Render everything here (All tab)
             this.$el.html(this.template(this.model.toJSON()));
             this.$el.toggleClass('highlight', this.model.get('isActive') && !this.model.get('isEditingName') );
             this.input = this.$('.edit'); 
           }
      return this;
    },

  // Toggle the `"active"` state of the model (Used for highlighting)
  toggleIsActive: _.throttle(function(){
            if ( ! this.model.get("isEditingName") )
                 this.model.toggleActive();
                 this.trigger('itemSelected');
               }, 300), // This is the double click speed (only goes lower than default)

  toggleImportant: function(){ 
           this.model.toggleImportant();
           this.model.save("isImportant");
            },

    // Switch this view into `"editing"` mode, displaying the input field.
    edit: function(event) {
      this.model.setEditingName();
      this.$el.addClass("editing");
      //Remove input focus to use multi edit mode in the management tree
      this.input.focus(); 
    },

    // Close the `"editing"` mode, saving changes to the Game.
    close: function() {
      var value = this.input.val();
      if ( value ) { // Do not let an empty name get saved
        this.model.save({GameName: value, isEditingName: false});
        this.$el.removeClass("editing");
      }
    },

    // If you hit `enter`, we're through editing the item.
    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.close();
    },

    // Remove the item, destroy the model.
    clear: function() {
      this.model.destroy(); // ! This wiil destroy the model in the database as well
    }

  });


//      this.model.set('GameName', this.model.get("GameName")+" "+Games.indexOf(this.model))



  var playGameView = Backbone.View.extend({
    tagName:  "div",
    template: _.template($('#game-board-template').html()),

    events: {
      "click .square" : "playerMove"
    },

    // The GameView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Game** and a **GameView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
      this.on('itemSelected', this.render);
    },

    render: function() {
      if ( this.model.get('isActive') ) {
	      this.$el.html(this.template(this.model.toJSON()) );
                    }
       else {
              this.$('#game_container').remove(); }
		var f = this.model.get('allMoves');
		for ( var a = 0; a < 9; a++ ) 
            if ( f[a] )
                 if ( f[a] == "player" ) 
                      this.$('#sq'+a).addClass("playerSymbol"); 
                 else this.$('#sq'+a).addClass("aiSymbol"); 

      return this;
    },


	player_move: function (square) {

        var g = this.model.get('allMoves')
        g[square] = "player";
		var ai_play = ai_move(parseInt(square));
        g[ai_play] = "ai";
        this.model.set('allMoves', g)
        this.model.allmoves_save(g);

  	    this.render();  // this is inefficient. Use element in playermove
	//	return ai_play;

	},

    playerMove: function(event) {
       this.player_move(parseInt($(event.currentTarget).attr("number")))
       this.$(event.currentTarget).addClass("playerSymbol");
		//$('#sq'+ai_play).addClass("aiSymbol");

    },

});



















// The view to operate the Game nav tabs
  var GameNavTabView = Backbone.View.extend({
    tagName:  "div",
    template: _.template($('#Game-nav-tabs-template').html()),
    events: {
      "click #all_tab"      : "toggleTab",
      "click #recent_tab"      : "toggleTab",
      "click #lost_tab"      : "toggleTab"
    },
    render: function() {
	      this.$el.html(this.template() );
              this.$el.find( '#'+this.model.get("navTab") ).addClass('active');
      return this;
    },
    toggleTab: function(ev) { 
         var tab_id =  $(ev.currentTarget).attr('id');
         Games.forEach(function(model){  // This is a little hack-ish, saves navTab into all Games/Models
             model.save({"navTab": tab_id}); // It would be better to use a single model and link it into the tree view
            });
         this.$el.has('ul').find('.active').removeClass("active");
         this.$el.find('#'+tab_id).addClass('active');
    },
  });



  // The Game Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#Gameapp"), //This does some neat things with the template rendering
    
    // Our template for the line of statistics at the bottom of the app.
    statsTemplate: _.template($('#stats-template').html()),
    // Delegated events for creating new items, and clearing completed ones.
    events: {
      "click #new-Game":  "createOnClick",
      "click #clear-selected": "clearSelected",
    },

    // At initialization we bind to the relevant events on the `Games`
    // collection, when items are added or changed. Kick things off by
    // loading any pre-existing Games that might be saved in *localStorage*.
    initialize: function() {

      this.listenTo(Games, 'add', this.addOne);
      this.listenTo(Games, 'reset', this.addAll);
      this.listenTo(Games, 'all', this.render);

      this.playGame = this.$('play_game_main');
      this.header = this.$('header');
      this.footer = this.$('footer');
      this.main = $('#main');

      Games.fetch();
    },

    // Re-rendering the App just means refreshing the statistics -- the rest
    // of the app doesn't change.
    render: function() { // Control the custom HTML tags here, e.g. <footer_section>
      var activeGames = Games.isActive().length;

      if ( Games.length )
         {
          this.main.show();
          this.header.show();
          this.footer.show();
          this.footer.html(this.statsTemplate({isActive: activeGames, isEditingName: Games.isEditingName().length}));
          this.playGame.show();
         }
      else {
             this.main.hide();
             this.footer.hide();
             this.playGame.hide(); // Turn off nav tabs if there are no Games
           }

    },

    // Add a single todo item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(Game) {
      var treeView = new GameView({model: Game});
      this.$("#Game-list").append(treeView.render().el);
      var gameView = new playGameView({model: Game});
      this.$("#play-area").append(gameView.render().el);
      var navView = new GameNavTabView({model: Game}); // Make sure that the nav tabs are rendered
      this.$("#Game_nav_tabs").html(navView.render().el);
 // every time a Game is created
  
    },

    // Add all items in the **Games** collection at once.
    addAll: function(Game) {    // Used when the page refreshes to re-add all models
      Games.each(this.addOne);  //  loads Games from database with the fetch() above
    },

    // If you click the plus button in the Game Management, create a new **Game* model,
    // persisting it to *localStorage*.
    createOnClick: function(e) {
           Games.create(); // Give us a fresh Game
     // this.input.val('');
    },

    // Clear all done Game items, destroying their models.
    clearSelected: function() {
      _.invoke(Games.isActive(), 'destroy'); // Triggers the destroy listener for every active Game model
      return false;
    },

  });

  // Finally, we kick things off by creating the **App**.
  var App = new AppView;
}); // The end of the DOM Ready header at the very top



















