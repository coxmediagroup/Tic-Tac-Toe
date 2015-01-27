
/**
* Main server script.
*/

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var t = require('./lib/tictactoeserver');


var board = null;             // Current tic-tac-toc board state. Also keeps track of who played previously.

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  socket.emit('updateMsg', 'Welcome! Lets player a game of Tic-Tac-Toe!');
  board = t.getBoardStateSample()
  socket.emit('updateBoard', board);
  setTimeout(function(){console.log('settimeout'); socket.emit('updateMsg', 'Your turn to make a move.');}, 3000);
  
  

  socket.on('nextMove', function(nmove){
    // 1) First determine whether the game is complete: [draw, humanWins, machineWins].

    console.log('player made a move ' + nmove.cellIdx + ' ' + nmove.player);

    // If nextMove valid, update the board:
    board = t.updateBoard(board, nmove);

    console.log('from server:'); console.log(board);

    socket.emit('updateBoard', board);

    if (nmove.player != 'machine') {
      // Let the machine player make a move:
      // 1) Machine makes a move.
      var nmove2 = null;
      nmove2 = t.getMPNextMoveRandom(board);
      console.log(nmove2);

      //   Update the board state on the server:
      board = t.updateBoard(board, nmove2);

      // 2) Update the boardUI on the client:
      socket.emit('updateBoard', board);  // Here, board.playerBefore == 'machine'. 
      // 3) Update msg:
      socket.emit('updateMsg', 'Your turn to make a move.');
    }
  });


});

http.listen(4000, function(){
  console.log('listening on *:4000');
});

