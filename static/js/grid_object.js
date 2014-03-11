function grid(x,y, indexInGridsArray, app_parent) {
	var self = this;
	
	self.x				= x;
	self.y				= y;
	self.value 			= ko.observable(0);	
	self.index			= indexInGridsArray;
	
	self.value.subscribe(function(newValue) {
	
		if( newValue === 1) {
			app_parent.humanIsFreeToSelect = false;
			app_parent.computer.humanPlays.push(self.index);
			app_parent.switchTurns();
		} else if( newValue === -1) {
			app_parent.computer.computerPlays.push(self.index);	
			app_parent.switchTurns();					
		}				
	});
	
	self.userClicked= function() {
		if(app_parent.humans_turn() && self.value() === 0 && app_parent.humanIsFreeToSelect){
			self.value(1);
		}
	}		
	
	self.imageClass = ko.computed(function(){
		//hides image tag when there's no image
	
		if(self.value() === 0) {
			return 'notShown';
		} else {
			return 'shown';
		}
	
	});
	
	self.image 	= ko.computed(function() {

			//sets the image for grid
			if( self.value() === 0 ){
			
				return '';				
			}else if( self.value() === 1){
			
				if( app_parent.play_as() === 'obama') {
					return 'static/images/obama.png';
				}else {
					return 'static/images/putin.png';
				}					
			}else if( self.value() === -1){
		
				if( app_parent.play_as() === 'obama') {
					return 'static/images/putin.png';
				}else {
					return 'static/images/obama.png';
				}
			}

		});
	
	self.enabled 	= ko.computed(function() {
			//enable grid if its the players turn and grid is not yet selected
			if( app_parent.humans_turn() === true && self.value() === 0 ){
				return 'enabled';				
			}else{
				return '';
			}
		});	


	

}	