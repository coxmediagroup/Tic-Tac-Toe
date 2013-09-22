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
		$( "#debug-out" ).append( stateGame.GetTime() + message + "\n" );
	},
	
	TrackMove: function( message )
	{
		$( "#move-tracker" ).append( message );
	},
	
	TrackWin: function( player )
	{
		if ( player != "none" )
		{
			$( "#move-tracker" ).append( player + " won round " + stateGame.turnInfo.timesPlayed + "\n" );
		}
		else
		{
			$( "#move-tracker" ).append( "There was a tie for round " + stateGame.turnInfo.timesPlayed + "\n" );
		}
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
		
		else if ( stateGame.turnInfo.turnCount == 1 )
		{			
			// Computer is responding to first movement
			if ( stateGame.turnInfo.lastMove == 4 )
			{
				// Player marked center, mark a corner
				var rand = parseInt( Math.random() * 4 );
				if ( rand == 0 ) 
				{
					if ( objGrid.RandomGrid( 0, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 0;
						this.ToggleTurns();
						return;
					}
				}
				else if ( rand == 1 )
				{
					if ( objGrid.RandomGrid( 2, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 2;
						this.ToggleTurns();
						return;
					}

				}
				else if ( rand == 2 )
				{
					if ( objGrid.RandomGrid( 6, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 6;
						this.ToggleTurns();
						return;
					}

				}
				else if ( rand == 3 )
				{
					if ( objGrid.RandomGrid( 8, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 8;
						this.ToggleTurns();
						return;
					}

				}
			}
			else 
			{
				// Player didn't mark center, mark the center for self.
				if ( objGrid.RandomGrid( 4, "computer" ) ) 
				{
					stateGame.turnInfo.lastMove = 4;
					this.ToggleTurns();
					return;
				}
			}
		}
		
		// Logic for other moves - At this point, the center is definitely taken.
		else 
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
				
			// 3. Try to make good move
			stateGame.DebugMessage( "No winning positions, try to make good move" );
			var lastMoveType = objGrid.EdgeOrCorner( stateGame.turnInfo.lastMove );
			if ( lastMoveType == "edge" )
			{
				// Mark a corner that isn't in the same row/column
				var moved = false;
				var rand = parseInt( Math.random() * 2 );
				
				if ( stateGame.turnInfo.lastMove == 3 )
				{
					if ( rand == 0 && objGrid.RandomGrid( 2, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 2;
						this.ToggleTurns();
						moved = true;
						return;
					}
					else if ( rand == 1 && objGrid.RandomGrid( 8, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 8;
						this.ToggleTurns();
						moved = true;
						return;
					}
				}
				else if ( stateGame.turnInfo.lastMove == 5 )
				{
					if ( rand == 0 && objGrid.RandomGrid( 0, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 0;
						this.ToggleTurns();
						moved = true;
						return;
					}
					else if ( rand == 1 && objGrid.RandomGrid( 6, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 6;
						this.ToggleTurns();
						moved = true;
						return;
					}
				}
				else if ( stateGame.turnInfo.lastMove == 1 )
				{
					if ( rand == 0 && objGrid.RandomGrid( 6, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 6;
						this.ToggleTurns();
						moved = true;
						return;
					}
					else if ( rand == 1 && objGrid.RandomGrid( 8, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 8;
						this.ToggleTurns();
						moved = true;
						return;
					}
				}
				else if ( stateGame.turnInfo.lastMove == 7 )
				{
					if ( rand == 0 && objGrid.RandomGrid( 0, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 0;
						this.ToggleTurns();
						moved = true;
						return;
					}
					else if ( rand == 1 && objGrid.RandomGrid( 2, "computer" ) ) 
					{
						stateGame.turnInfo.lastMove = 2;
						this.ToggleTurns();
						moved = true;
						return;
					}
				}
				
				if ( moved == false )
				{
					// Couldn't move to an ideal position - random?
					this.RandomStrategy( "computer" );
					return;
				}
			}
			else if ( lastMoveType == "corner" )
			{
				// Try to mark opposite corner
				if ( stateGame.turnInfo.lastMove == 0 && objGrid.RandomGrid( 8, "computer" ) )
				{
					stateGame.turnInfo.lastMove = 8;
					this.ToggleTurns();
					return;
				}
				else if ( stateGame.turnInfo.lastMove == 2 && objGrid.RandomGrid( 6, "computer" ) )
				{
					stateGame.turnInfo.lastMove = 6;
					this.ToggleTurns();
					return;
				}
				else if ( stateGame.turnInfo.lastMove == 6 && objGrid.RandomGrid( 2, "computer" ) )
				{
					stateGame.turnInfo.lastMove = 2;
					this.ToggleTurns();
					return;
				}
				else if ( stateGame.turnInfo.lastMove == 8 && objGrid.RandomGrid( 0, "computer" ) )
				{
					stateGame.turnInfo.lastMove = 0;
					this.ToggleTurns();
					return;
				}
				else
				{
					// Unable to mark opposite corner
					this.RandomStrategy( "computer" );
					return;
				}
			}
		}
	},
	
	RandomStrategy: function( player )
	{
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
