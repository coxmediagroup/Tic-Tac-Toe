// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){
  // Profile Model
  var Profile = Backbone.Model.extend({

    defaults: function() {
      return {
        profileName: "New Game",
        order: Profiles.nextOrder(),
        isActive: false,
        isEditingName: false,
	summery: '',
	fName: '',
        important: false,
        navTab: "all_tab"
      };
    },

    initialize: function() {
      if ( !this.get("profileName") ) 
        this.set({"profileName": this.defaults().profileName});   },

    toggleActive: function() {
      this.save({isActive: !this.get("isActive")});  },

    toggleImportant: function() {
      this.save({important: !this.get("important")});  },

    setEditingName: function() {
      this.save({isEditingName: true}); },

  });

  // Profile Collection
  // ---------------

  // The collection of characters is backed by *localStorage* instead of a remote server.
  var ProfileList = Backbone.Collection.extend({
    // Reference to this collection's model.
    model: Profile,
    // Save all of the Profile items under the `profile-backbone` namespace.
    localStorage: new Backbone.LocalStorage("profile-backbone"),
    // Filter down the list of all Character items that are alive.
    isActive: function() {
      return this.filter(function(profile){ return profile.get('isActive'); });
    },

    isImportant: function() {
      return this.filter(function(profile){ return profile.get('important'); });
    },
    // Filter down the list to only todo items that are still not finished.
    remaining: function() {
      return this.without.apply(this, this.isActive());
    },

    isEditingName: function() {
      return this.filter(function(profile){ return profile.get('isEditingName'); });
    },



    // We keep the Profiles in sequential order, despite being saved by unordered
    // GUID in the database. This generates the next order number for new items.
    nextOrder: function() {
      if (!this.length) return 1;
      return this.last().get('order') + 1;
    },

      // Profiles are sorted by their original insertion order.
    comparator: function(profile) {
      return profile.get('order');
    }

  });

  // Create our global collection of **Profiles**.
  var Profiles = new ProfileList;

  var ProfileView = Backbone.View.extend({
    tagName:  "li",
    // Cache the template function for a single item.
    template: _.template($('#profile-tree-template').html()),

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
  
    // Re-render the Profile management tree
    render: function() {
       if ( this.model.get("navTab") == "lost_tab" && !this.model.get("important") )
         {  // Remove all profiles from the list which are not marked (Important tab)
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

    // Close the `"editing"` mode, saving changes to the profile.
    close: function() {
      var value = this.input.val();
      if ( value ) { // Do not let an empty name get saved
        this.model.save({profileName: value, isEditingName: false});
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



  var ProfileEditView = Backbone.View.extend({
    tagName:  "li",
    template: _.template($('#profile-edit-template').html()),

    events: {
      "keypress .edit_summery"  : "updateOnEnter", //Todo: Add a better mechinism to use the Profile data
      "blur .edit_summery"      : "close",         //      This only handles the summery field
      "click .edit_summery"      : "edit"
    },

    // The ProfileView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Profile** and a **ProfileView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
      this.on('itemSelected', this.render);
    },

    render: function() {
      if ( this.model.get('isActive') ) {
	      this.$el.html(this.template(this.model.toJSON()) );
	      this.input = this.$('.edit_summery'); }
       else {
              this.$('#edit_profile_container').remove(); }
      return this;
    },

    // Switch this view into `"editing"` mode, displaying the input field.
    edit: function(event) {
      this.$el.addClass("editing");
      this.input.focus();
    },

    // Close the `"editing"` mode, saving changes to the todo.
    close: function() {
      var value = this.input.val();
        this.model.save({summery: value});
        this.$el.removeClass("editing");
    },

    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.close();
    },

});



// The view to operate the profile nav tabs
  var ProfileNavTabView = Backbone.View.extend({
    tagName:  "div",
    template: _.template($('#profile-nav-tabs-template').html()),
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
         Profiles.forEach(function(model){  // This is a little hack-ish, saves navTab into all Profiles/Models
             model.save({"navTab": tab_id}); // It would be better to use a single model and link it into the tree view
            });
         this.$el.has('ul').find('.active').removeClass("active");
         this.$el.find('#'+tab_id).addClass('active');
    },
  });



  // The Profile Application
  // ---------------

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#profileapp"), //This does some neat things with the template rendering
    
    // Our template for the line of statistics at the bottom of the app.
    statsTemplate: _.template($('#stats-template').html()),
    // Delegated events for creating new items, and clearing completed ones.
    events: {
      "click #new-profile":  "createOnClick",
      "click #clear-selected": "clearSelected",
    },

    // At initialization we bind to the relevant events on the `Profiles`
    // collection, when items are added or changed. Kick things off by
    // loading any pre-existing profiles that might be saved in *localStorage*.
    initialize: function() {

      this.listenTo(Profiles, 'add', this.addOne);
      this.listenTo(Profiles, 'reset', this.addAll);
      this.listenTo(Profiles, 'all', this.render);

      this.profileEdit = this.$('edit_profile_main');
      this.header = this.$('header');
      this.footer = this.$('footer');
      this.main = $('#main');

      Profiles.fetch();
    },

    // Re-rendering the App just means refreshing the statistics -- the rest
    // of the app doesn't change.
    render: function() { // Control the custom HTML tags here, e.g. <footer_section>
      var activeProfiles = Profiles.isActive().length;

      if ( Profiles.length )
         {
          this.main.show();
          this.header.show();
          this.footer.show();
          this.footer.html(this.statsTemplate({isActive: activeProfiles, isEditingName: Profiles.isEditingName().length}));
          this.profileEdit.show();
         }
      else {
             this.main.hide();
             this.header.hide();
             this.footer.hide();
             this.profileEdit.hide(); // Turn off nav tabs if there are no Profiles
           }

    },

    // Add a single todo item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(profile) {
      var treeView = new ProfileView({model: profile});
      this.$("#profile-list").append(treeView.render().el);
      var editView = new ProfileEditView({model: profile});
      this.$("#edit-list").append(editView.render().el);
      var navView = new ProfileNavTabView({model: profile}); // Make sure that the nav tabs are rendered
      this.$("#profile_nav_tabs").html(navView.render().el); // every time a profile is created
    },

    // Add all items in the **Profiles** collection at once.
    addAll: function(profile) {    // Used when the page refreshes to re-add all models
      Profiles.each(this.addOne);  //  loads Profiles from database with the fetch() above
    },

    // If you click the plus button in the Profile Management, create a new **Profile* model,
    // persisting it to *localStorage*.
    createOnClick: function(e) {
           Profiles.create(); // Give us a fresh profile
     // this.input.val('');
    },

    // Clear all done profile items, destroying their models.
    clearSelected: function() {
      _.invoke(Profiles.isActive(), 'destroy'); // Triggers the destroy listener for every active Profile model
      return false;
    },

  });

  // Finally, we kick things off by creating the **App**.
  var App = new AppView;
}); // The end of the DOM Ready header at the very top



















