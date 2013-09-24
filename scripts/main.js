// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

stateGame = {	
	turnInfo : {},

	Setup: function( settings, images )
	{
		objLogger.DebugMessage( "Main setup", 4 );
		
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
		stateGame.turnInfo.checkedWinner = false;
		
		objLogger.DebugMessage( "Computer Movement: " 	+ stateGame.turnInfo.computer, 4 );
		objLogger.DebugMessage( "Player Movement: " 	+ stateGame.turnInfo.player, 4 );
		objLogger.DebugMessage( "First turn: " 			+ stateGame.turnInfo.turn, 4 );
		
		// Add movement option change tracker
		$( "input:radio[name='computer-movement']" ).change( function() 
		{
			stateGame.turnInfo.computer = $(this).val();			
			objLogger.DebugMessage( "Computer movement set to " + stateGame.turnInfo.computer, 4 );
		} );
		
		$( "input:radio[name='player-movement']" ).change( function() 
		{
			stateGame.turnInfo.player = $(this).val();
			objLogger.DebugMessage( "Player movement set to " + stateGame.turnInfo.player, 4 );
		} );
	},

	HandleMouseDown: function( ev )
	{
		if ( stateGame.turnInfo.turn == "player" )
		{
			objPlayers.ManualPlayerMove ( ev, settings );
		}
	},

	Update: function( settings )
	{
		if ( stateGame.turnInfo.checkedWinner == false )	// Don't continue if we're waiting on reset timeout.
		{
			if ( stateGame.turnInfo.turn == "computer" )
			{
				if ( stateGame.turnInfo.computer == "strategy" )
				{
					objPlayers.ComputerStrategy();
				}
				else if ( stateGame.turnInfo.computer == "random" )
				{
					objPlayers.RandomStrategy( "computer" );
				}
			}
			else if ( stateGame.turnInfo.turn == "player" && stateGame.turnInfo.player == "random" )
			{
				objPlayers.RandomStrategy( "player" );
			}
			
			// Check to see if anyone won this round, or if there are no blocks left.
			this.CheckForWinner();
		}
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
		objLogger.DebugMessage( "Reset Game", 4 );	
		
		stateGame.turnInfo.firstMove	= stateGame.turnInfo.turn;
		stateGame.turnInfo.timesPlayed += 1;
		
		stateGame.turnInfo.checkedWinner = false;
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
		objLogger.DebugMessage( "Turn " + stateGame.turnInfo.turnCount + ": " + stateGame.turnInfo.turn, 4 );
	},
	
	CheckForWinner: function() 
	{
		if ( stateGame.turnInfo.checkedWinner == true )
		{
			// Prevent score from adding again and a second timeout from being created
			return;
		}
		
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
				objLogger.DebugMessage( "Tie", 4 );
			}
			
			objLogger.TrackWin( whoWon );			
			stateGame.turnInfo.checkedWinner = true;
					
			setTimeout( function() { 			
				stateGame.ResetGame( settings );
			}, 500 );
		}
	}
}
