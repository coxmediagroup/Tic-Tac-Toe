// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

/*
 * Handler class for player and computer
 * Functions:
 * ManualPlayerMove
 * RandomStrategy
 * ComputerStrategy
 * */

objPlayers = {

	/* When player clicks board, this is called to handle move position
	 * and trying to claim that tile.
	 * */
	ManualPlayerMove: function( ev, settings ) 
	{
		// Need to find coordinates based on canvas window position
		var mouseX = ev.clientX - $( "#cnvWindow" ).position().left;
		var mouseY = ev.clientY - $( "#cnvWindow" ).position().top;
		
		// Returns false if no item added
		if ( mouseX >= 0 && mouseX <= settings.width && mouseY >= 0 && mouseY <= settings.height &&
			objGrid.ClickedGrid( mouseX, mouseY, "player" ) )
		{
			stateGame.turnInfo.lastMove = objGrid.GetIndexAtPosition( mouseX, mouseY );
			stateGame.ToggleTurns();
		}
		
		stateGame.CheckForWinner();
	},

	/*
	 * If the random checkbox is selected for a player, this function
	 * is called to choose a random tile, with NO strategy.
	 * Useful for testing.
	 * */
	RandomStrategy: function( player )
	{		
		var randBlock = parseInt( Math.random() * 9 );
		
		if ( objGrid.TryMoveAtIndex( randBlock, player ) ) 
		{
			stateGame.turnInfo.lastMove = randBlock;
			stateGame.ToggleTurns();
		}
	},
	
	/* Imperfect computer strategy.  If the computer always goes first,
	 * the computer will always win.
	 * Otherwise, there is some chance the player will win.
	 * */
	ComputerStrategy: function()
	{		
		objLogger.DebugMessage( "--- Computer ---", 1 );	
		objLogger.DebugMessage( "--- Turn " + stateGame.turnInfo.turnCount + " ---", 1 );	
			
		// First Move logic
		if ( stateGame.turnInfo.turnCount == 0 )
		{
			objLogger.DebugMessage( "First move logic", 1 );

			// Computer is moving first, mark center block
			if ( objGrid.TryMoveAtIndex( 4, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = 4;
				stateGame.ToggleTurns();
				return;
			}
		}		
				
		// Logic for other moves - At this point, the center is definitely taken.
		// Trying logic from http://www.youtube.com/watch?v=C07jkOu9Tsc video:
		// Take position to the RIGHT of player if possible
		// Take position to the LEFT of player if possible
		// Take position to the ABOVE of player if possible
		// Take position to the BOTTOM of player if possible
		else if ( stateGame.turnInfo.firstMove == "computer" )
		{		
			objLogger.DebugMessage( "Computer controls the center", 1 );		
			objLogger.DebugMessage( "Check for Computer win position", 1 );
			// 1. Try to find a win position for computer
			var winPos = objGrid.FindWinIndex( "computer" );
			if ( winPos != -1 )
			{
				if ( objGrid.TryMoveAtIndex( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			objLogger.DebugMessage( "Check for Player win position", 1 );
			// 2. Try to block a win position from player
			var winPos = objGrid.FindWinIndex( "player" );
			if ( winPos != -1 )
			{
				if ( objGrid.TryMoveAtIndex( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			// These are only used if the check is passed. No grid wrap-around.
			var toRight 	= stateGame.turnInfo.lastMove+1;
			var toLeft 		= stateGame.turnInfo.lastMove-1;
			var toTop 		= stateGame.turnInfo.lastMove-3;
			var toBottom 	= stateGame.turnInfo.lastMove+3;
				
			// Try to take position to the right
			if ( 	stateGame.turnInfo.lastMove % 3 < 2 && 
					objGrid.TryMoveAtIndex( toRight, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toRight;
				objLogger.DebugMessage( "RIGHT: " + toRight, 2 );
				stateGame.ToggleTurns();
				return;
			}
			// Try to take position to the left
			else if ( 	stateGame.turnInfo.lastMove % 3 > 0 &&
						objGrid.TryMoveAtIndex( toLeft, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toLeft;
				objLogger.DebugMessage( "LEFT: " + toLeft, 2 );
				stateGame.ToggleTurns();
				return;
			}
			// Try to take position above
			else if ( 	parseInt( stateGame.turnInfo.lastMove / 3 ) > 0 &&
						objGrid.TryMoveAtIndex( toTop, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toTop;
				objLogger.DebugMessage( "TOP: " + toTop, 2 );
				stateGame.ToggleTurns();
				return;
			}
			
			// Try to take position below
			else if ( 	parseInt( stateGame.turnInfo.lastMove / 3 ) < 2 &&
						objGrid.TryMoveAtIndex( toBottom, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toBottom;
				objLogger.DebugMessage( "BOTTOM: " + toBottom, 2 );
				stateGame.ToggleTurns();
				return;
			}
			
			else
			{
				// TODO: Handle this better
				this.RandomStrategy( "computer" );
			}
		}
		else
		{
			// This is the logic for when the player controls the center tile because they went first
			// and chose the center tile on their first turn (otherwise the computer would have grabbed it)
			objLogger.DebugMessage( "Player controls the center", 1 );
			
			objLogger.DebugMessage( "Check for Computer win position", 1 );
			// 1. Try to find a win position for computer
			var winPos = objGrid.FindWinIndex( "computer" );
			if ( winPos != -1 )
			{
				if ( objGrid.TryMoveAtIndex( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			objLogger.DebugMessage( "Check for Player win position", 1 );
			// 2. Try to block a win position from player
			var winPos = objGrid.FindWinIndex( "player" );
			if ( winPos != -1 )
			{
				if ( objGrid.TryMoveAtIndex( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			
			objLogger.DebugMessage( "Take corner opposite to one controlled by the player", 1 );
			
			// Control corners. Mark a corner close to the player's last move if possible.
			// Prevent player from having two opposite corners
			if ( objGrid.WhoControls( 0 ) == "player" )
			{
				objLogger.DebugMessage( "Player controls NW", 1 );
				
				var tileToMove = 8;
				if ( objGrid.TryMoveAtIndex( tileToMove, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = tileToMove;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			if ( objGrid.WhoControls( 2 ) == "player" )
			{
				objLogger.DebugMessage( "Player controls NE", 1 );
				
				var tileToMove = 6;
				if ( objGrid.TryMoveAtIndex( tileToMove, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = tileToMove;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			if ( objGrid.WhoControls( 6 ) == "player" )
			{
				objLogger.DebugMessage( "Player controls SW", 1 );
				
				var tileToMove = 2;
				if ( objGrid.TryMoveAtIndex( tileToMove, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = tileToMove;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			if ( objGrid.WhoControls( 8 ) == "player" )
			{
				objLogger.DebugMessage( "Player controls SE", 1 );
				
				var tileToMove = 0;
				if ( objGrid.TryMoveAtIndex( tileToMove, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = tileToMove;
					stateGame.ToggleTurns();
					return;
				}
			}
			
			objLogger.DebugMessage( "Find intersecting corner", 1 );
			
			// Check any corners that the player already has a mark in that row/column
			var neighbors = {};
			var indexMax = 0;
			for ( var tileToMove = 0; tileToMove < 9; tileToMove += 2 )
			{
				if ( tileToMove != 4 )
				{
					var row = tileToMove % 3;
					var col = parseInt( tileToMove / 3 );
					var neighborCount = 0;
					
					for ( var r = col; r < 9; r += 3 )
					{
						if ( objGrid.WhoControls( r ) == "player" )
						{
							neighborCount++;
						}
					}
					
					for ( var c = row * 3; c < row * 3 + 3; c++ )
					{
						if ( objGrid.WhoControls( c ) == "player" )
						{
							neighborCount++;
						}
					}
					
					objLogger.DebugMessage( neighborCount + " neighbors for corner " + tileToMove, 1 );
					
					neighbors.tileToMove = neighborCount;
					if ( neighbors[tileToMove] > neighbors[indexMax] )
					{
						indexMax = tileTomove;
						objLogger.DebugMessage( "Max is " + indexMax, 1 );
					}
				}
			}
			
			objLogger.DebugMessage( "Max is " + indexMax, 1 );
			
			if ( objGrid.TryMoveAtIndex( indexMax, "computer" ) )
			{
				stateGame.turnInfo.lastMove = indexMax;
				stateGame.ToggleTurns();
				return;
			}
				
			objLogger.DebugMessage( "Capture center if available", 1 );
			
			if ( objGrid.WhoControls( 4 ) == "empty" )
			{		
				if ( objGrid.TryMoveAtIndex( 4, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = 4;
					stateGame.ToggleTurns();
					return;
				}
			}			
				
			objLogger.DebugMessage( "Capture other corner", 1 );
			
			// Otherwise, try to capture another corner
			for ( var tileToMove = 0; tileToMove < 9; tileToMove += 2 )
			{
				if ( tileToMove != 4 )
				{
					if ( objGrid.TryMoveAtIndex( tileToMove, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = tileToMove;
						stateGame.ToggleTurns();
						return;
					}
				}
			}
			
			objLogger.DebugMessage( "COMPUTER could not figure out good strategy.", 1 );
			
			// TODO: Handle this better
			objPlayers.RandomStrategy( "computer" );	
			
			return;
		}
	}
}
