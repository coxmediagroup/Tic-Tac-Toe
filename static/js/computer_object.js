function computersLogic(app_parent) {
	/*
		This object represents the brain or mind of the computer.
		It describes how the computer sees or perceives the grid and how it makes its decisions
		about which grid to play.
	*/
		
	var self = this;
	
	/*
		mind of computer stores the location of the center, corners, edges in the table.grids array.
		This is how the computer perceives the tic tac toe grid. With this level of abstraction, the 
		computer can make intelligent decisions to win or tie the game
	*/
	
	self.center 	= [4];
	self.corners	= [0, 2, 6, 8];
	self.edges		= [1, 3, 7, 5];		
	
	//this is how long the computer takes to make a decision
	self.decideTime	= 2000;
	
	self.computerPlays		= [];
	self.humanPlays			= [];
	
	self.strategy;
	
	//there are 8 different ways to win, 3 columns, 3 rows and 2 diagonals
	self.winningGridCombinations	= [[0,3,6],[1,4,7],[2,5,8],[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6]];
	
	self.randomNumberBetweenZeroAndN	= function(n) {
	
		//this will help the computer choose a random number
		return randomnumber=Math.floor(Math.random()*(n+1)) ;
	}
	
	
	self.getLastItemInArray		= function(array) {
		return array[array.length - 1];
	}
	
	
	self.classifyPlayType	= function(playSelection) {

		result = self.center.indexOf(playSelection);
		if( result !== -1) {
			return 'center';
		}
		
		result = self.corners.indexOf(playSelection);
		if( result !== -1) {
			return 'corner';
		}
		
		result = self.edges.indexOf(playSelection);
		if( result !== -1) {
			return 'edge';
		}

	}
	
	self.sharesSideWith		= function(gridA, gridB)
	{
		
		//function returns true if grid A shares side with grid B
		
		if (gridA.x === gridB.x) 
		{
			if (gridA.y === (gridB.y + 1) || gridA.y === (gridB.y - 1) )
			{
				//gridA and girdB share a horizontal edge
				return true;
			}
				
		} else if(gridA.y === gridB.y) 
		{
			if (gridA.x === (gridB.x + 1) || gridA.x === (gridB.x - 1) ) 
			{
				//gridA and girdB share a vertical edge
				return true;
			}
		}
		return false;
	}
	
	
	self.isDiagonalWith	= function(gridA, gridB)
	{
		
		//function returns true if grid A is on the  opposite diagonal of grid B
		//if the deltax and deltay = width of the row, then the two elements are opposite diagonals

		if(  ( Math.abs(gridA.x - gridB.x) === 2) &&  (Math.abs(gridA.y - gridB.y) === 2) ) {
			return true;
		}
		return false;
	}				
		
	
	
	self.makeFirstPlayAttackMode = function() {
	
		//computer uses random number to choose strategy
		var technique = self.randomNumberBetweenZeroAndN(1);
		
		if( technique === 0 ) {
			//select center
			app_parent.table.grids[ self.center[0] ].value(-1);
			
			
		} else {
			//select a corner randomly
			
			corner = self.randomNumberBetweenZeroAndN(3);
			app_parent.table.grids[ self.corners[corner] ].value(-1);
		}							
		
	}
	
	self.makeSecondPlayAttackMode = function() {
	
		//find out what move the human last made
		humanPreviousPlayIndex 		= self.getLastItemInArray( self.humanPlays );
		
		//classify humans last play
		humanPreviousPlayType 	= self.classifyPlayType(humanPreviousPlayIndex);
		
		//uses humanPreviousPlayIndex to find the last actual grid selected
		lastGridHumanSelected 	= app_parent.table.grids[ humanPreviousPlayIndex ];
		
		computerPreviousPlayIndex	= self.getLastItemInArray( self.computerPlays );  
		lastGridComputerSelected 	= app_parent.table.grids[ computerPreviousPlayIndex ];
		
		
		if( humanPreviousPlayType === 'edge') {
			//the computer will select a corner which does not share a side with the human's previous play
			
			nonSideSharingCorners = [];
			for(i=0; i< self.corners.length; i++) {
			
				if( app_parent.table.grids[ self.corners[i] ].value() !== 0) {
					//if grid has been selected, then skip it
					continue;
				}
			
				localGrid = app_parent.table.grids[ self.corners[i] ];
				if( self.sharesSideWith(lastGridHumanSelected, localGrid) === false ) {
					nonSideSharingCorners.push(self.corners[i]);
				}
			}
			
			
			//if center is not taken, then choose corner that is not diagonal to the the computers 1st selection
			if (app_parent.table.grids[4].value() ===0) {
				
				for(i=0; i<nonSideSharingCorners.length; i++) {
					localGrid = app_parent.table.grids[ nonSideSharingCorners[i] ];
					
					if( self.isDiagonalWith(lastGridComputerSelected, localGrid) === false ) {
						selectedCornerIndex = nonSideSharingCorners[i];
						break;
					}
				}
				
					//computer takes the index and uses it to select a corner
					app_parent.table.grids[ selectedCornerIndex ].value(-1);	
					
			} else {
			
				//computer randomly chooses a corner from the non sharing side corners
				selectedCornerIndex = self.randomNumberBetweenZeroAndN(nonSideSharingCorners.length - 1);
				
				//computer takes the index and uses it to select a corner
				app_parent.table.grids[ nonSideSharingCorners[selectedCornerIndex] ].value(-1);						
				
			}
			

			

		}else if (humanPreviousPlayType === 'center') {
			//the computer will select the corner opposite from its previous selection
			
			var diagonalCorner;
			
			for(i=0; i< self.corners.length; i++) {
			
				if( app_parent.table.grids[ self.corners[i] ].value() !== 0) {
					//if grid has been selected, then skip it
					continue;
				}
			
				localGrid = app_parent.table.grids[ self.corners[i] ];
				if( self.isDiagonalWith(lastGridComputerSelected, localGrid) ) {
					diagonalCorner = self.corners[i];
					break;
				}
			}
			
			//computer takes the index and uses it to select a corner
			app_parent.table.grids[ diagonalCorner ].value(-1);
			
		
		}else if (humanPreviousPlayType === 'corner') {
		
			//computer will select from the non-diagonal corners
			nonDiagonalCorners = [];
			
			for(i=0; i< self.corners.length; i++) {
			
				if( app_parent.table.grids[ self.corners[i] ].value() !== 0) {
					//if grid has been selected, then skip it
					continue;
				}
			
				localGrid = app_parent.table.grids[ self.corners[i] ];
				if( self.isDiagonalWith(lastGridHumanSelected, localGrid) === false ) {
					nonDiagonalCorners.push(self.corners[i]);
				}
			}
			//computer randomly chooses a corner from the non sharing side corners
			selectedCornerIndex = self.randomNumberBetweenZeroAndN(nonDiagonalCorners.length - 1);
			
			//computer takes the index and uses it to select a corner
			app_parent.table.grids[ nonDiagonalCorners[selectedCornerIndex] ].value(-1);
			
		}
	
	}
	
	self.makeSecondPlayAttackModeForCornerCornerDiagonal = function(){
		//returns true if situation meets criteria and computer is able to select
		
		if( self.computerPlays.length === 2) {
			//checks to see if first two computer selections were corners
			computerIndex0	= self.computerPlays[0];  
			computerIndex1	= self.computerPlays[1];  
			
			computerIndexType0 	= self.classifyPlayType(computerIndex0);
			computerIndexType1 	= self.classifyPlayType(computerIndex1);
			
			if(computerIndexType0 === 'corner' && computerIndexType1 === 'corner'){
			
				acceptValue = true;
			
				for(i=0; i< self.corners.length; i++) {

					corner = self.corners[i];	
					localCornerGrid	= 	app_parent.table.grids[ corner ];
					gridValue	=	app_parent.table.grids[ corner ].value();					
					
					if(gridValue ===0) {
						//corner has not been chosen yet
						
						for(j=0; j< self.humanPlays.length; j++) {
						
							//uses humanPreviousPlayIndex to find the last actual grid selected
							localHumanGrid 	= app_parent.table.grids[ j ];
							
							if(self.sharesSideWith(localHumanGrid, localCornerGrid)) {
								acceptValue = false;
							}
						
						}	
						
						if(acceptValue === true) {
							app_parent.table.grids[ corner ].value(-1);
							return true;
						}
					
					}
				}
			}

		}
		return false;				
	}
	
	
	self.makeFirstPlayDefenseMode = function() {
		//find out what move the human last made
		humanPreviousPlayIndex 		= self.getLastItemInArray( self.humanPlays );
		//classify humans last play
		humanPreviousPlayType 	= self.classifyPlayType(humanPreviousPlayIndex);
		
		if (humanPreviousPlayType === 'center' ) 
		{
			//the computer will select any corner 
			selectedCornerIndex = self.randomNumberBetweenZeroAndN( self.corners.length - 1);
			
			//computer takes the index and uses it to select a corner
			app_parent.table.grids[ self.corners[selectedCornerIndex] ].value(-1);
		} else if (humanPreviousPlayType === 'corner' || humanPreviousPlayType === 'edge' ) {
		
			//when opponent selects corner, select the center
			app_parent.table.grids[ 4 ].value(-1);				
		}
	}
	
	
	self.makeSecondPlayDefenseMode = function() {	
		
		//find out what move the human currently made
		humanPreviousPlayIndex 		= self.getLastItemInArray( self.humanPlays );

		computerPreviousPlayIndex 		= self.getLastItemInArray( self.computerPlays );
		//classify humans current play
		computerPreviousPlayType 	= self.classifyPlayType(computerPreviousPlayIndex);				

				

		if(  ([0,2,6,8].indexOf(humanPreviousPlayIndex) !== -1) && computerPreviousPlayType === 'center' ) {
			//this is a "corner corner-diagonal" situation
			
			if(self.steadyStateAlgorithm()) {}
			else{
				self.selectRemainingEdges();
			}					
		} else {
		
			//for all other situations:
			//the computer will select something to block opponent or select a corner
			if(self.steadyStateAlgorithm()) {}
			else{
				self.selectRemainingCorners();
			}				
		}

	
	}			
	
	self.selectRemainingCorners = function() {
		//function returns true if it selected grid and false otherwise			
		//computer tries to select any unselected corners first
		for(i=0; i< self.corners.length; i++) {
			corner = self.corners[i];
			gridValue	=	app_parent.table.grids[ corner ].value();
			
			if(gridValue === 0) {
				//corner has not been choosen yet
				
				//select corner and return
				app_parent.table.grids[ corner ].value(-1);
				return true;
			}
		}
		return false;
	}

	self.selectRemainingEdges = function() {
		//function returns true if it selected grid and false otherwise
		//computer tries to select any unselected edges after,
		//note that at this point, the center would have already been selected
		for(i=0; i< self.edges.length; i++) {
			edge = self.edges[i];
			gridValue	=	app_parent.table.grids[ edge ].value();
			
			if(gridValue === 0) {
				//edge has not been choosen yet
				
				//select edge and return
				app_parent.table.grids[ edge ].value(-1);
				return true;
			}
		}
		return false;
	}
	
	
	self.findMissingElements = function(winningArray, negationValue) {
		/*
			function returns an array of grids not yet clicked on
			but if that array has a value of negationValue, the entire row has to be negated
		*/
		
		missingElements = [];
		for(j=0; j<winningArray.length; j++) {

			gridValue	=	app_parent.table.grids[ winningArray[j] ].value();
			if( gridValue === 0) {
				
				missingElements.push(winningArray[j]);
			} else if(gridValue === negationValue) {
				return [];
			}
		}
		return missingElements;
	}
	
	self.returnElementNeededToWin = function(negationValue){
		//function returns the index (in app.table.grids) of the element needed to win or false if there is none
		for(i=0; i<self.winningGridCombinations.length; i++) {

			missingElements = self.findMissingElements(self.winningGridCombinations[i], negationValue);
			if(missingElements.length == 1) {
				//there is only one more element in this winning combination that is needed to win
				//return the index of that element
				return missingElements[0];
			}
		}
		
		//In all winning combinations, there is more than one element needed to win
		return false;
	}
	
	
	
	self.steadyStateAlgorithm = function() {
		//function returns true if it selected grid and false otherwise
	
		//check to see if computer can win the game
		computerIndex = self.returnElementNeededToWin(1);
		humanIndex = self.returnElementNeededToWin(-1);
		
		if(computerIndex !== false) {
			//computer selects last item it needs to win
			app_parent.table.grids[ computerIndex ].value(-1);
			return true;					
			
		} else if(humanIndex !== false){
			//computer blocks user by selecting item she needs to win
			app_parent.table.grids[ humanIndex ].value(-1);
			return true;
		} 
		
		return false;
		

	
	}


}
