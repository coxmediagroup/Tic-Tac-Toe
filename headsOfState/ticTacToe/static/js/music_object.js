function musicControl() {

	//---------------------------------------------controls music
	var self				= this;
	self.musicOn			= ko.observable(true);	
	
	if(window.location.hash=== "#main" || window.location.hash=== "") {
		self.onMain	= ko.observable(true);	
	} else {
		self.onMain	= ko.observable(false);		
	}
	
	self.toggleMusic = function() {
	//clicking music on-off toggles musicOn
		self.musicOn( !self.musicOn() );	
		self.addOrUpdateMusic();		

	}	
	
	self.toggleOnMain = function() {
	//clicking the settings button toggles onMain
		self.onMain( !self.onMain() );
		self.addOrUpdateMusic();	
	}	
	
	self.removeMusic = function() {

		var element = document.getElementById("music");
		if(element !== null){
			element.parentNode.removeChild(element);
		}
	}

	self.addOrUpdateMusic = function() {

		//makes sure to remove music if it existed
		self.removeMusic();
		
		//add music only if music is on
		if( self.musicOn() ){
			if( self.onMain()=== true){
				file = "static/sounds/music1.mp3";
			} else {
				file = "static/sounds/music2.mp3";		
			}
			music = "<embed id='music' src="+file+" autostart='true' loop='true' hidden='true'>";
			
			var parentElement = document.getElementById("musicContainer");
			parentElement.innerHTML = parentElement.innerHTML + music;		
		}

	}
	self.addOrUpdateMusic();
	//---------------------------------------------controls music	
	

	}
	
	
