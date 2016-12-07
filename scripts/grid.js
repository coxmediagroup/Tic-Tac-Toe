// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

/*
 * objGrid class for handling board / possible movements.
 * Functions:
 * Setup
 * Update
 * Draw
 * GetIndexAtPosition
 * ClickedGrid
 * TryMoveAtIndex
 * EdgeOrCorner
 * EmptyBlocksLeft
 * WhoWon
 * FindWinIndex
 * LogBoard
 * */

objGrid = {
	
	/*
	 * Initializes the game board, clears out all states
	 * */
	Setup: function( settings ) 
	{
		this.gridData = new Array();
		
		this.gridWidth = 100;
		this.gridHeight = 100;
	
		for ( var i = 0; i < 9; i++ )
		{
			this.gridData[i] = new Array();
			this.gridData[i].x = (i % 3) * this.gridWidth + 10;
			this.gridData[i].y = parseInt( i / 3 ) * this.gridHeight + 10;
			this.gridData[i].state = "empty";
		}
	},
	
	Update: function( settings ) 
	{
	},
	
	/*
	 * Draws the board to the HTML5 canvas
	 * */
	Draw: function( canvasWindow, settings, images ) 
	{
		
		for ( var i = 0; i < this.gridData.length; i++ )
		{
			canvasWindow.fillStyle = "#fbedcd";
			canvasWindow.fillRect( this.gridData[i].x, this.gridData[i].y, this.gridWidth, this.gridHeight );
			canvasWindow.strokeStyle = "#000000";
			canvasWindow.strokeRect( this.gridData[i].x, this.gridData[i].y, this.gridWidth, this.gridHeight );
			
			if ( this.gridData[i].state == "player" ) 
			{
				canvasWindow.drawImage( images.x, this.gridData[i].x, this.gridData[i].y, 100, 100 );
			}
			else if ( this.gridData[i].state == "computer" ) 
			{
				canvasWindow.drawImage( images.o, this.gridData[i].x, this.gridData[i].y, 100, 100 );
			}
		}
		
	},
	
	/*
	 * Translates (x,y) coordinates into an index in the 1-D array of tiles
	 * */
	GetIndexAtPosition: function( x, y )
	{
		return parseInt( x / 100 ) + parseInt( y / 100 ) * 3;
	},
	
	/*
	 * Receives (x,y) coordinates and tries to see if that tile is available
	 * Returns true if move was success; fail if tile is already taken.
	 * */
	ClickedGrid: function( mouseX, mouseY, player ) 
	{
		// Figure out which grid this is
		var index = this.GetIndexAtPosition( mouseX, mouseY );
		
		return this.TryMoveAtIndex( index, player );
	},
	
	/*
	 * Returns whether "player" or "computer" or "empty" controls this tile
	 * */
	WhoControls: function( index ) 
	{
		return this.gridData[index].state;
	},
	
	/*
	 * Checks to see whether tile is available, and if it is will claim it
	 * for the current player moving.
	 * */
	TryMoveAtIndex: function( index, player ) 
	{
		if ( index < 0 || index > 8 )
		{
			return false;
		}
		
		objLogger.DebugMessage( player + " trying to move to " + index, 3 );
		if ( this.gridData[index].state == "empty" )
		{
			objLogger.DebugMessage( "Set block " + index + " to " + player, 3 );
			this.gridData[index].state = player;
			
			objLogger.DebugMessage( "Move success", 3 );
			
			return true;
		}
		
		objLogger.DebugMessage( "Move failure", 3 );
		
		return false;
	},
	
	/*
	 * Checks to see whether the tile at the given index is an edge,
	 * corner, or center tile.
	 * */
	EdgeOrCorner: function( index ) 
	{
		if ( index % 2 != 0 )
		{
			return "edge";
		}
		else if ( index % 2 == 0 && index != 4 )
		{
			return "corner";
		}
		else
		{
			return "center";
		}
	},
	
	/*
	 * Returns the amount of tiles still in the "empty" state.
	 * */
	EmptyBlocksLeft: function()
	{
		var emptyCount = 0;
		for ( var i = 0; i < this.gridData.length; i++ )
		{
			if ( this.gridData[i].state == "empty" )
			{
				emptyCount++;
			}
		}
		
		return emptyCount;
	},
	
	/*
	 * Checks to see if there are any winners. Will return "none" if
	 * nobody wins. The main state will know whether there are any empty
	 * spaces left, and will call it a tie. Otherwise, the game will continue.
	 * */
	WhoWon: function() 
	{
		/*
		 * Win Conditions:
		 * i, i+1, i+2 for i % 3 == 0 (Horizontal)
		 * i, i+3, i+6 for i / 3 == 0 (Vertical)
		 * i, i+4, i+8 for i == 0 (Diagonal Top-Left to Bottom-Right)
		 * i, i+2, i+4 for i == 2 (Diagonal Top-Right to Bottom-Left)
		 * */
		 
		// Horizontal check
		for ( var y = 0; y <= 6; y += 3 )
		{
			if ( 	this.gridData[y].state == this.gridData[y+1].state &&
					this.gridData[y].state == this.gridData[y+2].state &&
					this.gridData[y].state != "empty" )
			{
				objLogger.DebugMessage( "** Horizontal win " + this.gridData[y].state, 4 );
				return this.gridData[y].state;
			}
		}

		// Vertical check
		for ( var x = 0; x < 3; x++ )
		{
			if ( 	this.gridData[x].state == this.gridData[x+3].state &&
					this.gridData[x].state == this.gridData[x+6].state &&
					this.gridData[x].state != "empty" )
			{
				objLogger.DebugMessage( "** Vertical win " + this.gridData[x].state, 4 );
				return this.gridData[x].state;
			}
		}

		// Diagonal 1
		if ( 	this.gridData[0].state == this.gridData[4].state &&
				this.gridData[0].state == this.gridData[8].state &&
				this.gridData[0].state != "empty" )
		{
			objLogger.DebugMessage( "** Diagonal 1 win " + this.gridData[0].state, 4 );
			return this.gridData[0].state;
		}


		// Diagonal 2
		if ( 	this.gridData[2].state == this.gridData[4].state && 
				this.gridData[2].state == this.gridData[6].state &&
				this.gridData[2].state != "empty" )
		{
			objLogger.DebugMessage( "** Diagonal 2 win " + this.gridData[2].state, 4 );
			return this.gridData[2].state;
		}
		
		return "none";
	},
	
	/*
	 * Tries to find any tiles that will give the player (passed in via argument)
	 * an immediate win
	 * */
	FindWinIndex: function( player )
	{				
		// Horizontal check
		for ( var y = 0; y <= 6; y += 3 )
		{
			var consecutiveMarks = 0;
			
			for ( var x = 0; x < 3; x++ )
			{
				if ( this.gridData[y+x].state == player ) 
				{
					consecutiveMarks++;
				}
			}	
			
			if ( consecutiveMarks == 2 )
			{
				// which element is empty?
				for ( var x = 0; x < 3; x++ )
				{
					if ( this.gridData[y+x].state == "empty" ) 
					{
						return y+x;
					}
				}	
			} 
		}
		
		// Vertical check
		for ( var x = 0; x < 3; x++ )
		{
			var consecutiveMarks = 0;
			
			for ( var y = 0; y <= 6; y += 3 )
			{
				if ( this.gridData[y+x].state == player ) 
				{
					consecutiveMarks++;
				}
			}
			
			if ( consecutiveMarks == 2 )
			{
				// which element is empty?
				for ( var y = 0; y <= 6; y += 3 )
				{
					if ( this.gridData[y+x].state == "empty" ) 
					{
						return y+x;
					}
				}	
			} 
		}
		
		// Diagonal Check 1
		var consecutiveMarks = 0;
		for ( var i = 0; i < 9; i += 4 )
		{
			if ( this.gridData[i].state == player ) 
			{
				consecutiveMarks++;
			}
		}
		
		if ( consecutiveMarks == 2 ) 
		{
			for ( var i = 0; i < 9; i += 4 )
			{
				if ( this.gridData[i].state == "empty" )
				{
					return i;
				}
			}
		}
		
		// Diagonal Check 2	
		var consecutiveMarks = 0;
		for ( var i = 2; i <= 6; i += 2 )
		{
			if ( this.gridData[i].state == player ) 
			{
				consecutiveMarks++;
			}
		}
		
		if ( consecutiveMarks == 2 ) 
		{
			for ( var i = 2; i <= 6; i += 2 )
			{
				if ( this.gridData[i].state == "empty" )
				{
					return i;
				}
			}
		}	
		
		objLogger.DebugMessage( "Could not find win position for " + player, 3 );
		return -1;
	},
	
	/*
	 * Logs the 3x3 grid via the logger so can keep track of each move
	 * in case the player wins.
	 * */
	LogBoard: function() 
	{
		objLogger.TrackMove( "\nROUND " + stateGame.turnInfo.timesPlayed + " turn " + stateGame.turnInfo.turnCount + ":\n" );
		for ( var i = 0; i < 9; i++ )
		{			
			if ( this.gridData[i].state == "player" )
			{
				objLogger.TrackMove( "P" );
			}
			else if ( this.gridData[i].state == "computer" )
			{
				objLogger.TrackMove( "C" );
			}
			else
			{
				objLogger.TrackMove( "-" );
			}
			
			if ( i == 2 || i == 5 || i == 8 ) 
			{
				objLogger.TrackMove( "\n" );
			}
		}
	}
}
