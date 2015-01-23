GameBoardTest = TestCase("GameBoardTest");

GameBoardTest.prototype.testCalculateSquareIndex = function(){
	var gameBoard = new GameBoard();
	assertEquals(0, gameBoard.calculateSquareIndex(0, 0));
	assertEquals(8, gameBoard.calculateSquareIndex(2, 2));
	assertEquals(2, gameBoard.calculateSquareIndex(0, 2));
	assertEquals(4, gameBoard.calculateSquareIndex(1, 1));
	assertEquals(6, gameBoard.calculateSquareIndex(2, 0));
};

GameBoardTest.prototype.testSetSquare = function(){
	var gameBoard = new GameBoard();
	
	gameBoard.setSquare(0, 0,'X');
	assertEquals('X', gameBoard.squares[0]);
	
	gameBoard.setSquare(1, 1,'O');
	assertEquals('O', gameBoard.squares[4]);
	
	assertEquals(' ', gameBoard.squares[2]);
};

GameBoardTest.prototype.testGetSquareSymbol = function(){
	var gameBoard = new GameBoard();

	assertEquals(' ', gameBoard.getSquareSymbol(0,0));

	gameBoard.setSquare(0, 0,'X');
	assertEquals('X', gameBoard.getSquareSymbol(0,0));

	gameBoard.setSquare(1, 1,'O');
	assertEquals('O', gameBoard.getSquareSymbol(1,1));
		
};