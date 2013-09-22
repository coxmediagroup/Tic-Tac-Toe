// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

function Setup( settings, images )
{
	objGrid.Setup( settings );
	images.pathbase = "assets/";
	
	images.x = new Image();
	images.x.src = images.pathbase + "x.png";
	
	images.o = new Image();
	images.o.src = images.pathbase + "o.png";
	
	turn = "player";
	
	settings.computer = "strategy";
	settings.player = "manual";
	
	// Add movement option change tracker
	$( "input:radio[name='computer-movement']" ).change( function() 
	{
		settings.computer = $(this).val();
		
		$( "#debug-out" ).html( settings.computer );
	} );
	
	$( "input:radio[name='player-movement']" ).change( function() 
	{
		settings.player = $(this).val();

		$( "#debug-out" ).html( settings.player );
	} );
}

function HandleMouseDown( ev )
{

}

function Update( settings )
{
	if ( turn == "computer" )
	{
		if ( settings.computer == "strategy" )
		{
		}
		else if ( settings.computer == "manual" )
		{
		}
	}
	else if ( turn == "player" && settings.player == "random" )
	{
	}
}

function Draw( canvasWindow, settings, images )
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
