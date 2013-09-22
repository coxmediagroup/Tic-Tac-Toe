$( document ).ready( function() 
{
	var settings = { width: 320, height: 320, fps: 30 };
	var images = new Array();

	$( "canvas" ).attr( "width", settings.width );
	$( "canvas" ).attr( "height", settings.height );
	
	var canvasWindow = $( "canvas" )[0].getContext( "2d" );
	
	// Loading Screen
	canvasWindow.fillStyle = "#398eed";
	canvasWindow.fillRect( 0, 0, settings.width, settings.height );
	canvasWindow.fillStyle = "#ffffff";
	canvasWindow.fillText( "Loading...", 10, 10 );
	
	window.addEventListener( "mousedown", stateGame.HandleMouseDown, false );
	
	stateGame.Setup( settings, images );
	
	setInterval( function() {
		stateGame.Update( settings );
		stateGame.Draw( canvasWindow, settings, images );
	}, 1000 / settings.fps );
} );
