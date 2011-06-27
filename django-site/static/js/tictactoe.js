/*
 * Just pass the html canvas and gameover-callback to the game.init() function
 * and you should be set!
 * 
 * Simplest implementation:
 * var game = new TicTacToe.game();
 * 
 * // pass true if you wish to play as X, false for O
 * game.init('html5-canvas', true, gameover, function(){
 * 	
 *    // code to run after game is finished initializing
 * 
 * }); 
 * 
 * function gameover(code) {
 * 	if(code == [TicTacToe.WIN | TicTacToe.LOSS | TicTacToe.TIE]) {
 * 	  //show message
 *  }
 * }
 */

TicTacToe = {
	
	WIN: 1,
	LOSS: 2,
	TIE: 3,
	
	game: function() {
		var self = this;
		this.canvasId = '';
		this.canvasWidth = 0;
		this.canvasHeight = 0;
		this.cellWidth = 0;
		this.cellHeight = 0;
		this.playerIsX = true;
		this.gameOverCallback = null;
		this.boardSize = 3;
		
		var click = function(e) {
			var canvas = $('#'+self.canvasId);
			var clickX = parseInt(e.pageX-canvas.offset().left);
			var clickY = parseInt(e.pageY-canvas.offset().top);
			var cellX = parseInt(clickX/self.cellWidth);
			var cellY = parseInt(clickY/self.cellHeight);
			mark(cellX, cellY);
		}
		
		// make a move for the player
		var mark = function(cellX, cellY) {
			$.post('/tictactoe/makemove/x/'+cellX+'/y/'+cellY,
				function(data) {
					if(data.success) {
						self.draw(self.playerIsX, cellX, cellY);
						if(data.win) {
							if(data.winner == 1) {
								self.gameOverCallback(TicTacToe.WIN);
							} else {
								self.gameOverCallback(TicTacToe.LOSE);
							}
						} else {
							getmove();
						}
					}
					else {
						alert(data.message);
						//self.gameOverCallback(TicTacToe.TIE);
					}
				},
				'json'
			);
		}
		
		// get the computer's next move
		var getmove = function() {
			$.post('/tictactoe/getmove/',
				function(data) {
					if(data.success) {
						self.draw(!self.playerIsX, data.x, data.y);
						if(data.win) {
							if(data.winner == 1) {
								self.gameOverCallback(TicTacToe.WIN);
							} else {
								self.gameOverCallback(TicTacToe.LOSE);
							}
						}
					} else {
						alert(data.message);
						//self.gameOverCallback(TicTacToe.TIE);
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
			var size = (self.cellWidth < self.cellHeight) ? (self.cellWidth-pad)/2 : (self.cellHeight-pad)/2;
			
			var canvas = document.getElementById(self.canvasId);
			var c = canvas.getContext('2d');
			
			c.beginPath();
			c.strokeStyle = 'blue';
			c.beginPath();
			c.arc(centerX, centerY, size, 0, Math.PI*2, true);
			c.closePath();
			c.stroke();
			
		}
		
		this.init = function(canvasId, playerIsX, gameOverCallback, returnCallback) {
			var canvas = $('#'+canvasId);
			self.canvasId = canvasId;
			self.canvasWidth = parseInt(canvas.attr('width'));
			self.canvasHeight = parseInt(canvas.attr('height'));
			self.cellWidth = parseInt(self.canvasWidth/self.boardSize);
			self.cellHeight = parseInt(self.canvasHeight/self.boardSize);
			
			canvas.bind('click', click);
			this.gameOverCallback = gameOverCallback;
			this.newGame(playerIsX, function(){ self.clearBoard() });
			returnCallback();
		}
		
		this.newGame = function(playerIsX, callback) {
			this.playerIsX = playerIsX;
			var xo = playerIsX ? 'x' : 'o';
			$.post('/tictactoe/newgame/size/'+self.boardSize+'/',
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
			c.strokeStyle = 'black';
			for(var i = 1; i <= self.boardSize; i++) {
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
}