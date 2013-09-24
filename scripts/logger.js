// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

debugLevel = 2;

/* Logger class
 * Logs game events to the textareas on the webpage 
 * Functions:
 * GetTime
 * DebugMessage
 * TrackMove
 * TrackWin
 * */
objLogger = {
	GetTime: function()
	{
		var time = new Date();
		return "[" + time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds() + "." + time.getMilliseconds() + "] ";
	},
	
	/*
	 * Debug messages are handy, it lets me know what the computer is 
	 * "thinking" on a given move.
	 * Also other program debug notes, but level 1 and 2 are more
	 * critical to the computer AI.
	 * */
	DebugMessage: function( message, level ) 
	{
		// debug level has 1 for highest, 0 for off, and lower numbers.
		if ( level <= debugLevel ) 
		{
			$( "#debug-out" ).append( objLogger.GetTime() + message + "\n" );
		}
	},
	
	/*
	 * Outputs the ASCII version of the game board
	 * */
	TrackMove: function( message )
	{
		$( "#move-tracker" ).append( message );
	},
	
	/*
	 * A win has occurred, log who won.
	 * */
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
			// We don't want to have a really long log, so we are only saving the data
			// for debug & turn tracking if the player happen to win this round.
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
