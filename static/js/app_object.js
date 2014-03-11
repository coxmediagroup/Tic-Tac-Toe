function app() {
	var self				= this;
	self.play_as 			= ko.observable('obama');	

	
	//----------------------------choose first turn
	/*
		humanIsFreeToSelect is used because without it, as the app is waiting to change turns,
		the human can select more than one grid
	 */
	
	if (Math.random() <= 0.5) {
		self.humans_turn 		= ko.observable(true);
		self.humanIsFreeToSelect= true;
		self.turnMessageStyle	= ko.observable('humanTurnMessage');	
	} else {
		self.humans_turn 		= ko.observable(false);
		self.humanIsFreeToSelect= false;
		self.turnMessageStyle	= ko.observable('computerTurnMessage');	
	}
	//----------------------------choose first turn			

	self.table	= new table(self);
	self.isOkayToReset = true;
	
	self.resetTable		= function() {
	
		if(self.isOkayToReset) {
			self.isOkayToReset = false;
			//function sets the value of all grids to 0
			for(i=0; i< self.table.grids.length; i++) {
				self.table.grids[i].value(0);
			}
			
			//toggles the turn, so the other player can play
			self.humans_turn( !self.humans_turn() );
			self.initializeApp();
			self.computer.computerPlays = [];
			self.computer.humanPlays = [];	
		}				
	}

	self.turnNotifier 	= ko.computed(function() {
	
			//gives the user feedback on who's turn it is
			if( self.humans_turn () === true ){
				self.turnMessageStyle('humanTurnMessage');	
				return "Your Play";				
			}else{
				self.turnMessageStyle('computerTurnMessage');	
				return "Opponent Play";
			}
		});	

	self.toggleSelectedCharacter	= function() {
		if(self.play_as() === 'obama') {
			self.play_as('putin');
		} else {
			self.play_as('obama');
		}
	}
	
	
	self.computer	= new computersLogic(self);
	
	self.initializeApp = function(){
		if( self.humans_turn() === false) {
			//------------------------when computer takes the first turn
			self.computer.strategy = 'attack';
			setTimeout(function(){
				//computer takes the index and uses it to select a corner
				self.computer.makeFirstPlayAttackMode();
			},self.computer.decideTime);	
			//-------------------------when computer takes the first turn				
		} else {
			self.computer.strategy = 'defend';
		}			
	}
	
	self.initializeApp();
	

	
	self.switchTurns = function() {
	
		setTimeout(function(){
			
			self.humans_turn(!self.humans_turn());
			
			//now when it is the humans turn, she can select again
			self.humanIsFreeToSelect = true;
			self.isOkayToReset = true;
			
			if(self.humans_turn()=== false) {
				if( self.computer.strategy === 'attack') {
				
					if(self.computer.computerPlays.length===1) {
						//when the computer has made one play already
						self.computer.makeSecondPlayAttackMode();
					} else if( self.computer.makeSecondPlayAttackModeForCornerCornerDiagonal() ){
						//this is for making the corner-corner diagonal better
					}else {
						//when the computer has made more than 2 moves with the attack strategy
						if(self.computer.steadyStateAlgorithm()) {}
						else if(self.computer.selectRemainingCorners()) { }
						else if(self.computer.selectRemainingEdges()) { }	
						}
						
				} else {
				
				
					if(self.computer.computerPlays.length===0) {
						self.computer.makeFirstPlayDefenseMode();
						
					} else if(self.computer.computerPlays.length===1) {
						self.computer.makeSecondPlayDefenseMode();
					} else {
						//when the computer has made more than 2 moves with the defense strategy
						
						if(self.computer.steadyStateAlgorithm()) {}
						else if(self.computer.selectRemainingCorners()) { }
						else if(self.computer.selectRemainingEdges()) { }								

					}
				}
			}					
			
		},1500);

	
	}
	

			
}


var vm = new app();
ko.applyBindings(vm);



	