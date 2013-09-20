// Rachel J. Morris - From https://github.com/coxmediagroup/Tic-Tac-Toe

function Setup( settings, images )
{
	objGrid.Setup( settings );
	images.pathbase = "assets/";
	
	images.x = new Image();
	images.x.src = images.pathbase + "x.png";
	
	images.o = new Image();
	images.o.src = images.pathbase + "o.png";
}

function HandleMouseDown( ev )
{
}

function Update( settings )
{
}

function Draw( canvasWindow, settings, images )
{
	// Draw background
	canvasWindow.fillStyle = "#654f1b";
	canvasWindow.fillRect( 0, 0, settings.width, settings.height );
	
	// Draw board grid
	objGrid.Draw( canvasWindow, settings );
	
	// Turn indicator
	canvasWindow.fillStyle = "#ffffff";
	canvasWindow.font = "20px Arial";
	canvasWindow.fillText( "Computer's turn", 10, 350 );
	
	// Placeholder - Draw an X and O
	canvasWindow.drawImage( images.x, 10, 10, 100, 100 );
	canvasWindow.drawImage( images.o, 110, 10, 100, 100 );
}
