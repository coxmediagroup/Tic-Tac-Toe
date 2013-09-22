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

	Setup: function( settings, images )
	{
		stateGame.DebugMessage( "Main setup" );
		
		objGrid.Setup( settings );		
		images.pathbase = "assets/";
		
		images.x = new Image();
		images.x.src = images.pathbase + "x.png";
		
		images.o = new Image();
		images.o.src = images.pathbase + "o.png";
		
		stateGame.turnInfo.turn 		= "player";		
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
			
			stateGame.DebugMessage( "Mouse click at (" + mouseX + ", " + mouseY + ")" );
			
			// Returns false if no item added
			if ( mouseX >= 0 && mouseX <= settings.width && mouseY >= 0 && mouseY <= settings.height &&
				objGrid.ClickedGrid( mouseX, mouseY, "player" ) )
			{
				stateGame.turnInfo.turn = "computer";
				stateGame.DebugMessage( "Turn: " + stateGame.turnInfo.turn );
			}
		}
	},

	Update: function( settings )
	{
		if ( stateGame.turnInfo.turn == "computer" )
		{
			if ( stateGame.turnInfo.computer == "strategy" )
			{
			}
			else if ( stateGame.turnInfo.computer == "random" )
			{
				var randBlock = parseInt( Math.random() * 9 );
				
				if ( objGrid.RandomGrid( randBlock, "computer" ) ) 
				{
					stateGame.turnInfo.turn = "player";
					stateGame.DebugMessage( "Turn: " + stateGame.turnInfo.turn );
				}
			}
		}
		else if ( stateGame.turnInfo.turn == "player" && stateGame.turnInfo.player == "random" )
		{
			var randBlock = parseInt( Math.random() * 9 );
			
			if ( objGrid.RandomGrid( randBlock, "player" ) ) 
			{
				stateGame.turnInfo.turn = "computer";
				stateGame.DebugMessage( "Turn: " + stateGame.turnInfo.turn );
			}
		}
		
		// Check to see if anyone won this round, or if there are no blocks left.
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
			
			
			// TODO: Make reset prettier / have user click before resetting game
			stateGame.ResetGame( settings );
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
		objGrid.Setup( settings );
		stateGame.DebugMessage( "Reset Game" );	
	}
}
