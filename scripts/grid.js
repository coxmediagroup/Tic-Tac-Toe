objGrid = {
	
	// 3x3 grid
	Setup: function( settings ) 
	{
		this.gridData = new Array();
		
		this.gridWidth = 100;
		this.gridHeight = 100;
	
		for ( var i = 0; i < 9; i++ )
		{
			this.gridData[i] = new Array();
			this.gridData[i].x = (i % 3) * this.gridWidth + 10;
			this.gridData[i].y = parseInt( i / 3 ) * this.gridHeight + 10;
			this.gridData[i].state = "empty";
		}
	},
	
	Update: function( settings ) 
	{
	},
	
	Draw: function( canvasWindow, settings, images ) 
	{
		
		for ( var i = 0; i < this.gridData.length; i++ )
		{
			canvasWindow.fillStyle = "#fbedcd";
			canvasWindow.fillRect( this.gridData[i].x, this.gridData[i].y, this.gridWidth, this.gridHeight );
			canvasWindow.strokeStyle = "#000000";
			canvasWindow.strokeRect( this.gridData[i].x, this.gridData[i].y, this.gridWidth, this.gridHeight );
			
			if ( this.gridData[i].state == "player" ) 
			{
				canvasWindow.drawImage( images.x, this.gridData[i].x, this.gridData[i].y, 100, 100 );
			}
			else if ( this.gridData[i].state == "computer" ) 
			{
				canvasWindow.drawImage( images.o, this.gridData[i].x, this.gridData[i].y, 100, 100 );
			}
		}
		
	},
	
	ClickedGrid: function( mouseX, mouseY, player ) 
	{
		// Figure out which grid this is
		var index = parseInt( mouseX / 100 ) + parseInt( mouseY / 100 ) * 3;
		
		return this.RandomGrid( index, player );
	},
	
	RandomGrid: function( index, player ) 
	{
		if ( this.gridData[index].state == "empty" )
		{
			stateGame.DebugMessage( "Set block " + index + " to " + player );
			this.gridData[index].state = player;
			
			return true;
		}
		
		return false;
	},
	
	EmptyBlocksLeft: function()
	{
		var emptyCount = 0;
		for ( var i = 0; i < this.gridData.length; i++ )
		{
			if ( this.gridData[i].state == "empty" )
			{
				emptyCount++;
			}
		}
		
		return emptyCount;
	}	
}
