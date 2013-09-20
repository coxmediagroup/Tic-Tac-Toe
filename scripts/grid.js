objGrid = {
	
	// 3x3 grid
	Setup: function( settings ) {
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
	
	Update: function( settings ) {
	},
	
	Draw: function( canvasWindow, settings ) {
		
		for ( var i = 0; i < this.gridData.length; i++ )
		{
			canvasWindow.fillStyle = "#fbedcd";
			canvasWindow.fillRect( this.gridData[i].x, this.gridData[i].y, this.gridWidth, this.gridHeight );
			canvasWindow.strokeStyle = "#000000";
			canvasWindow.strokeRect( this.gridData[i].x, this.gridData[i].y, this.gridWidth, this.gridHeight );
		}
		
	}
		
}
