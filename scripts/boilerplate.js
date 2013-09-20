$( document ).ready( function() 
{
	var settings = { width: 640, height: 480, fps: 30 };
	var images = {};
	var sounds = {};
	
	$( "canvas" ).attr( "width", settings.width );
	$( "canvas" ).attr( "height", settings.height );
	
	var canvasWindow = $( "canvas" )[0].getContext( "2d" );
	
	// Loading Screen
	canvasWindow.fillStyle = "#398eed";
	canvasWindow.fillRect( 0, 0, settings.width, settings.height );
	canvasWindow.fillStyle = "#ffffff";
	canvasWindow.fillText( "Loading...", 10, 10 );
	
	window.addEventListener( "mousedown", HandleMouseDown, false );
	
	Setup( settings );
	
	setInterval( function() {
		Update( settings );
		Draw( canvasWindow, settings );
	}, 1000 / settings.fps );
} );
