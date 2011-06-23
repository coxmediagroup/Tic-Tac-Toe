function TicTacToe() {
	
	var self = this;
	this.canvasId = '';
	this.canvasWidth = 0;
	this.canvasHeight = 0;
	this.cellWidth = 0;
	this.cellHeight = 0;
	this.playerIsX = true;
	
	var click = function(e) {
		var canvas = $('#'+self.canvasId);
		var clickX = parseInt(e.pageX-canvas.offset().left);
		var clickY = parseInt(e.pageY-canvas.offset().top);
		var cellX = parseInt(clickX/self.cellWidth);
		var cellY = parseInt(clickY/self.cellHeight);
		mark(cellX, cellY);
	}
	
	var mark = function(cellX, cellY) {
		$.post('/tictactoe/makemove/x/'+cellX+'/y/'+cellY,
			function(data) {
				if(data.success) {
					self.draw(self.playerIsX, cellX, cellY);
					if(data.win) {
						alert(data.winner+' wins!');
					} else {
						getmove();
					}
				}
				else {
					alert(data.message);
				}
			},
			'json'
		);
	}
	
	var getmove = function() {
		$.post('/tictactoe/getmove/',
			function(data) {
				if(data.success) {
					self.draw(!self.playerIsX, data.x, data.y);
					if(data.win) {
						alert(data.winner+' wins!');
					}
				} else {
					alert(data.message);
				}
			},
			'json'
		);
	}
	
	this.setPlayer = function(xo) {
		if(xo == 'x') {
			self.playerIsX = true;
			return true;
		} else if (xo == 'o') {
			self.playerIsX = false;
			return true;
		}
		return false;
	}
	
	this.draw = function(drawX, cellX, cellY) {
		if(drawX) {
			self.drawX(cellX, cellY);
		} else {
			self.drawO(cellX, cellY);
		}
	}
	
	this.drawX = function(cellX, cellY) {
		
		var pad = 10;
		var lft = cellX*self.cellWidth+pad;
		var rgt = (cellX+1)*self.cellWidth-pad;
		var top = cellY*self.cellHeight+pad;
		var btm = (cellY+1)*self.cellHeight-pad;
		
		var canvas = document.getElementById(self.canvasId);
		var c = canvas.getContext('2d');
		
		c.beginPath();
		c.strokeStyle = 'red';
		c.moveTo(lft, top);
		c.lineTo(rgt, btm);
		c.moveTo(lft, btm);
		c.lineTo(rgt, top);
		c.stroke();
		
	}
	
	this.drawO = function(cellX, cellY) {
		
		var pad = 10;
		var centerX = cellX*self.cellWidth+self.cellWidth/2;
		var centerY = cellY*self.cellHeight+self.cellHeight/2;
		
		var canvas = document.getElementById(self.canvasId);
		var c = canvas.getContext('2d');
		
		c.beginPath();
		c.strokeStyle = 'blue';
		c.beginPath();
		c.arc(centerX, centerY, 45, 0, Math.PI*2, true);
		c.closePath();
		c.stroke();
		
	}
	
	this.init = function(canvasId) {
		var canvas = $('#'+canvasId);
		self.canvasId = canvasId;
		self.canvasWidth = parseInt(canvas.attr('width'));
		self.canvasHeight = parseInt(canvas.attr('height'));
		self.cellWidth = parseInt(self.canvasWidth/3);
		self.cellHeight = parseInt(self.canvasHeight/3);
		
		canvas.bind('click', click);
	}
	
	this.newGame = function(playerIsX, callback) {
		this.playerIsX = playerIsX;
		var xo = playerIsX ? 'x' : 'o';
		$.post('/tictactoe/newgame/setplayer/'+xo,
			function(data) {
				if(data.success) {
					callback(true);
				} else {
					callback(false);
				}
			},
			'json'
		);
	},
	
	this.clearBoard = function() {
		
		var w = self.canvasWidth;
		var h = self.canvasHeight;
		var cw = self.cellWidth;
		var ch = self.cellHeight;
		
		var canvas = document.getElementById(self.canvasId);
		var c = canvas.getContext('2d');
		c.clearRect(0,0,w,h);
		for(var i = 1; i <= 3; i++) {
			c.beginPath();
			c.moveTo(i*cw,0);
			c.lineTo(i*cw,w);
			c.stroke();
			c.moveTo(0,i*ch);
			c.lineTo(h,i*ch);
			c.stroke();
		}
		
		if(!this.playerIsX) {
			getmove();
		}
	}
	
}
