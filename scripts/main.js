// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

stateGame = {	
	turnInfo : {},
	
	GetTime: function()
	{
		var time = new Date();
		return "[" + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds() + "." + time.getMilliseconds() + "] ";
	},
	
	DebugMessage: function( message ) 
	{
		//$( "#debug-out" ).append( stateGame.GetTime() + message + "\n" );
	},
	
	TrackMove: function( message )
	{
		//$( "#move-tracker" ).append( message );
	},
	
	TrackWin: function( player )
	{
		/*
		if ( player == "player" )
		{
			$( "#move-tracker" ).append( "!!!!!!!!!!!!!" + player + " won round " + stateGame.turnInfo.timesPlayed + "\n" );
		}
		else if ( player == "computer" )
		{
			$( "#move-tracker" ).append( player + " won round " + stateGame.turnInfo.timesPlayed + "\n" );
		}
		else
		{
			$( "#move-tracker" ).append( "There was a tie for round " + stateGame.turnInfo.timesPlayed + "\n" );
		}
		$( "#move-tracker" ).append( "________________________________________\n\n" );
		* */
	},

	Setup: function( settings, images )
	{
		stateGame.DebugMessage( "Main setup" );
		
		objGrid.Setup( settings );		
		images.pathbase = "assets/";
		
		images.x = new Image();
		images.x.src = images.pathbase + "x.png";
		
		images.o = new Image();
		images.o.src = images.pathbase + "o.png";
		
		stateGame.turnInfo.timesPlayed 	= 1;
		stateGame.turnInfo.turn 		= "player";		
		stateGame.turnInfo.firstMove	= stateGame.turnInfo.turn;
		stateGame.turnInfo.turnCount 	= 0;
		stateGame.turnInfo.lastMove 	= -1;
		stateGame.turnInfo.computer 	= $( "input:radio[name='computer-movement']" ).val();
		stateGame.turnInfo.player 		= $( "input:radio[name='player-movement']" ).val();
		stateGame.turnInfo.gameOver = "false";
		
		stateGame.DebugMessage( "Computer Movement: " 	+ stateGame.turnInfo.computer );
		stateGame.DebugMessage( "Player Movement: " 	+ stateGame.turnInfo.player );
		stateGame.DebugMessage( "First turn: " 			+ stateGame.turnInfo.turn );
		
		// Add movement option change tracker
		$( "input:radio[name='computer-movement']" ).change( function() 
		{
			stateGame.turnInfo.computer = $(this).val();			
			stateGame.DebugMessage( "Computer movement set to " + stateGame.turnInfo.computer );
		} );
		
		$( "input:radio[name='player-movement']" ).change( function() 
		{
			stateGame.turnInfo.player = $(this).val();
			stateGame.DebugMessage( "Player movement set to " + stateGame.turnInfo.player );
		} );
	},

	HandleMouseDown: function( ev )
	{
		if ( stateGame.turnInfo.turn == "player" )
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
		}
	},

	Update: function( settings )
	{
		if ( stateGame.turnInfo.turn == "computer" )
		{
			if ( stateGame.turnInfo.computer == "strategy" )
			{
				this.ComputerStrategy();
			}
			else if ( stateGame.turnInfo.computer == "random" )
			{
				this.RandomStrategy( "computer" );
			}
		}
		else if ( stateGame.turnInfo.turn == "player" && stateGame.turnInfo.player == "random" )
		{
			this.RandomStrategy( "player" );
		}
		
		// Check to see if anyone won this round, or if there are no blocks left.
		this.CheckForWinner();
	},

	Draw: function( canvasWindow, settings, images )
	{
		// Draw background
		canvasWindow.fillStyle = "#654f1b";
		canvasWindow.fillRect( 0, 0, settings.width, settings.height );
		
		// Draw board grid & X's & O's
		objGrid.Draw( canvasWindow, settings, images );
	},
	
	ResetGame: function( settings )
	{
		stateGame.turnInfo.turnCount = 0;
		objGrid.Setup( settings );
		stateGame.DebugMessage( "Reset Game" );	
		
		//stateGame.turnInfo.turn 		= "player";	
		stateGame.turnInfo.firstMove	= stateGame.turnInfo.turn;
	},
	
	ComputerStrategy: function()
	{		
		// First Move logic
		if ( stateGame.turnInfo.turnCount == 0 )
		{
			// Computer is moving first, mark center block
			if ( objGrid.RandomGrid( 4, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = 4;
				this.ToggleTurns();
				return;
			}
		}		
		
		else if ( stateGame.turnInfo.turnCount == 1 && stateGame.turnInfo.lastMove != 4 )
		{			
			// Computer is responding to first movement
			// Player didn't mark center, mark the center for self.
			if ( objGrid.RandomGrid( 4, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = 4;
				this.ToggleTurns();
				return;
			}
		}
		
		// stateGame.turnInfo.firstMove	= stateGame.turnInfo.turn;
		
		// Logic for other moves - At this point, the center is definitely taken.
		// Trying logic from http://www.youtube.com/watch?v=C07jkOu9Tsc video:
		// Take position to the RIGHT of player if possible
		// Take position to the LEFT of player if possible
		// Take position to the ABOVE of player if possible
		// Take position to the BOTTOM of player if possible
		else if ( 	stateGame.turnInfo.firstMove == "computer" || 
					( stateGame.turnInfo.firstMove == "player" && objGrid.WhoControls( 4 ) == "computer" ) )
		{		
			// 1. Try to find a win position for computer
			var winPos = objGrid.FindWinIndex( "computer" );
			if ( winPos != -1 )
			{
				if ( objGrid.RandomGrid( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					this.ToggleTurns();
					return;
				}
			}
			
			// 2. Try to block a win position from player
			var winPos = objGrid.FindWinIndex( "player" );
			if ( winPos != -1 )
			{
				if ( objGrid.RandomGrid( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					this.ToggleTurns();
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
					objGrid.RandomGrid( toRight, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toRight;
				stateGame.DebugMessage( "RIGHT: " + toRight );
				this.ToggleTurns();
				return;
			}
			// Try to take position to the left
			else if ( 	stateGame.turnInfo.lastMove % 3 > 0 &&
						objGrid.RandomGrid( toLeft, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toLeft;
				stateGame.DebugMessage( "LEFT: " + toLeft );
				this.ToggleTurns();
				return;
			}
			// Try to take position above
			else if ( 	parseInt( stateGame.turnInfo.lastMove / 3 ) > 0 &&
						objGrid.RandomGrid( toTop, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toTop;
				stateGame.DebugMessage( "TOP: " + toTop );
				this.ToggleTurns();
				return;
			}
			
			// Try to take position below
			else if ( 	parseInt( stateGame.turnInfo.lastMove / 3 ) < 2 &&
						objGrid.RandomGrid( toBottom, "computer" ) ) 
			{
				stateGame.turnInfo.lastMove = toBottom;
				stateGame.DebugMessage( "BOTTOM: " + toBottom );
				this.ToggleTurns();
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
			
			// 1. Try to find a win position for computer
			var winPos = objGrid.FindWinIndex( "computer" );
			if ( winPos != -1 )
			{
				if ( objGrid.RandomGrid( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					this.ToggleTurns();
					return;
				}
			}
			
			// 2. Try to block a win position from player
			var winPos = objGrid.FindWinIndex( "player" );
			if ( winPos != -1 )
			{
				if ( objGrid.RandomGrid( winPos, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					this.ToggleTurns();
					return;
				}
			}
			
			
			// Control corners
			for ( var i = 0; i <= 8; i += 2 )
			{
				stateGame.DebugMessage( "CORNER: " + i );
					if ( i != 4 && objGrid.RandomGrid( i, "computer" ) )
					{
						stateGame.turnInfo.lastMove = i;
						stateGame.DebugMessage( "MOVED TO CORNER: " + i );
						this.ToggleTurns();
						return;
					}
			}
			
			
			// TODO: Handle this better
			this.RandomStrategy( "computer" );
			return;
		}
	},
	
	RandomStrategy: function( player )
	{
		if ( player == "player" ) 
		{
			var winPos = objGrid.FindWinIndex( "player" );
			if ( winPos != -1 )
			{
				if ( objGrid.RandomGrid( winPos, "player" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					this.ToggleTurns();
					return;
				}
			}
			
			var winPos = objGrid.FindWinIndex( "computer" );
			if ( winPos != -1 )
			{
				if ( objGrid.RandomGrid( winPos, "player" ) ) 
				{
					stateGame.turnInfo.lastMove = winPos;
					this.ToggleTurns();
					return;
				}
			}
			
			if ( objGrid.WhoControls( 4 ) == "empty" && objGrid.RandomGrid( 4, "player" ) )
			{
				stateGame.turnInfo.lastMove = 4;
				this.ToggleTurns();
				return;
			}
		}
		
		var randBlock = parseInt( Math.random() * 9 );
		
		if ( objGrid.RandomGrid( randBlock, player ) ) 
		{
			stateGame.turnInfo.lastMove = randBlock;
			this.ToggleTurns();
		}
	},
	
	ToggleTurns: function() 
	{		
		if ( stateGame.turnInfo.turn == "player" ) 
		{
			stateGame.turnInfo.turn = "computer";
		}
		else
		{
			stateGame.turnInfo.turn = "player";
		}
		
		objGrid.LogBoard();
		
		stateGame.turnInfo.turnCount++;
		stateGame.DebugMessage( "Turn " + stateGame.turnInfo.turnCount + ": " + stateGame.turnInfo.turn );
	},
	
	CheckForWinner: function() 
	{
		var whoWon = objGrid.WhoWon();
		if ( objGrid.EmptyBlocksLeft() == 0 || whoWon != "none" ) 
		{						
			// Update score data
			if ( whoWon == "player" ) 			
			{ 
				$( "#wins-player" ).html( parseInt( $( "#wins-player" ).html() ) + 1 ); 
			}
			else if ( whoWon == "computer" ) 	
			{ 
				$( "#wins-computer" ).html( parseInt( $( "#wins-computer" ).html() ) + 1 ); 
			}
			else 								
			{ 
				$( "#wins-ties" ).html( parseInt( $( "#wins-ties" ).html() ) + 1 );
				stateGame.DebugMessage( "Tie" );
			}
			
			objGrid.LogBoard();
			stateGame.TrackWin( whoWon );
			stateGame.turnInfo.timesPlayed++;			
			
			// TODO: Make reset prettier / have user click before resetting game
			stateGame.ResetGame( settings );
		}
	}
}
