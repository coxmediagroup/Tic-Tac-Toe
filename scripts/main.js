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
			}
		}
		else if ( stateGame.turnInfo.turn == "player" && stateGame.turnInfo.player == "random" )
		{
		}
	},

	Draw: function( canvasWindow, settings, images )
	{
		// Draw background
		canvasWindow.fillStyle = "#654f1b";
		canvasWindow.fillRect( 0, 0, settings.width, settings.height );
		
		// Draw board grid
		objGrid.Draw( canvasWindow, settings );
		
		// Placeholder - Draw an X and O
		canvasWindow.drawImage( images.x, 10, 10, 100, 100 );
		canvasWindow.drawImage( images.o, 110, 10, 100, 100 );
	}
}
