var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendfile('index.html');
});

io.on('connection', function(socket){
  console.log('Starting Game');
  gamestate = [0,0,0,0,0,0,0,0,0]
  socket.on('disconnect', function(){
    console.log('Game Finished / Exited');
  });
  socket.on('player_move', function(input){
    // check if input is legal (hasn't already been picked)
    if (gamestate[input] === 0) {
      
      // it's a legal move, and let's add it to the game state
      gamestate[input] = 1;

      // check to see if the player won
      if (check_for_win(gamestate, 'player')){
        
        // if they've won, you've messed up
        io.emit('player_move', { pos: input, msg: 'You Won!', state: gamestate, player: 'player'});

      } else {
        // if they've failed to win, continue your AIs quest for glory

        ai_input = ai_turn(gamestate);
        gamestate[ai_input] = 2;
        console.log(gamestate + ' | ' + ai_input)
        

        if (check_for_win(gamestate, 'AI')){
          // we've won
          ai_move_msg = 'The AI Won Suckah!';
        } else {
          ai_move_msg = 'The AI picked position ' + ai_input
        }

        // still need to show their turn, but immediately take the AI turn afterwards
        io.emit('player_move', { pos: input, msg: 'You picked position ' + input, state: gamestate, player: 'player'});
        io.emit('player_move', { pos: ai_input, msg: ai_move_msg, state: gamestate, player: 'AI'});

      }
    } else {
    //  the move is illegal  
      io.emit('player_move', { pos: 9, msg: 'illegal manuever - please choose another position', state: gamestate, player: 'player'})
    }
    
  });
});

function check_for_win(gamestate, player){
  if (player === 'AI'){
    player = 2
  } else {
    player = 1
  }
  //  012
  if (gamestate[0] == player && gamestate[1] == player && gamestate[2] == player) {
    return true;
  }
  // 048
  else if (gamestate[0] == player && gamestate[4] == player && gamestate[8] == player) {
    return true;
  }
  // 036
  else if (gamestate[0] == player && gamestate[3] == player && gamestate[6] == player) {
    return true;
  }
  // 147
  else if (gamestate[1] == player && gamestate[4] == player && gamestate[7] == player) {
    return true;
  }
  // 258
  else if (gamestate[2] == player && gamestate[5] == player && gamestate[8] == player) {
    return true;
  }
  // 345
  else if (gamestate[3] == player && gamestate[4] == player && gamestate[5] == player) {
    return true;
  }
  // 678
  else if (gamestate[6] == player && gamestate[7] == player && gamestate[8] == player) {
    return true;
  }
  // 246
  else if (gamestate[2] == player && gamestate[4] == player && gamestate[6] == player) {
    return true;
  } else {
    return false;
  }
}

function ai_turn(gamestate){
  if (gamestate[4] == 0) {
    return 4;
  } else if (gamestate[0] == 0) {
    return 0;
  } else if (gamestate[2] == 0) {
    return 2;
  } else if (gamestate[6] == 0) {
    return 6;
  } else if (gamestate[8] == 0) {
    return 8;
  } else if (gamestate[1] == 0) {
    return 1;
  } else if (gamestate[3] == 0) {
    return 3;
  } else if (gamestate[5] == 0) {
    return 5;
  } else if (gamestate[8] == 0) {
    return 8;
  }
}

http.listen(3000, function(){
  console.log('listening on *:3000');
});