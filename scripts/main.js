// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

function Setup( settings )
{
}

function HandleKeyDown( ev )
{
}

function HandleKeyUp( ev )
{
}

function HandleMouseDown( ev )
{
}

function Update( settings )
{
}

function Draw( canvasWindow, settings )
{
	// Draw background
	canvasWindow.fillStyle = "#654f1b";
	canvasWindow.fillRect( 0, 0, settings.width, settings.height );
	
	// Draw board grid
	canvasWindow.fillStyle = "#fbedcd";
	canvasWindow.fillRect( 640/2-50, 480/2-50, 100, 100 );
	canvasWindow.strokeStyle = "#000000";
	canvasWindow.strokeRect( 640/2-50, 480/2-50, 100, 100 );
}
