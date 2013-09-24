debugLevel = 2;

/* Logs game events to the textareas on the webpage */
objLogger = {
	GetTime: function()
	{
		var time = new Date();
		return "[" + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds() + "." + time.getMilliseconds() + "] ";
	},
	
	DebugMessage: function( message, level ) 
	{
		// debug level has 1 for highest, 0 for off, and lower numbers.
		if ( level <= debugLevel ) 
		{
			$( "#debug-out" ).append( objLogger.GetTime() + message + "\n" );
		}
	},
	
	TrackMove: function( message )
	{
		$( "#move-tracker" ).append( message );
	},
	
	TrackWin: function( player )
	{
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
		
		if ( player == "player" )
		{
			// Copy contents of this tracker to the debug log before clearing the log.
			$( "#debug-player-win" ).append( "\n-------------------------------------------\n" );
			$( "#debug-player-win" ).append( "\n\nROUND DEBUG" );
			$( "#debug-player-win" ).append( $( "#debug-out" ).html() );
			
			$( "#debug-player-win" ).append( "\nROUND MOVES" );
			$( "#debug-player-win" ).append( $( "#move-tracker" ).html() );
		}
		
		$( "#move-tracker" ).empty();
		$( "#debug-out" ).empty();
		
	}
};
