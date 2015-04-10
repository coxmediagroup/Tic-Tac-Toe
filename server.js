var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var path = require('path');

app.use(express.static('public'));

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname,'./public/index.html'));
});

io.on('connection', function(socket){
  console.log('Starting Game');
  gamestate = [0,0,0,0,0,0,0,0,0];
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
        reset_game();

      } else {
        // if they've failed to win, continue your AIs quest for glory

        ai_input = ai_turn(gamestate, input);
        gamestate[ai_input] = 2;

        ai_move_msg = 'The AI picked position ' + ai_input
        // still need to show their turn, but immediately take the AI turn afterwards
        io.emit('player_move', { pos: input, msg: 'You picked position ' + input, state: gamestate, player: 'player'});
        io.emit('player_move', { pos: ai_input, msg: ai_move_msg, state: gamestate, player: 'AI'});
        
        if (check_for_win(gamestate, 'AI')){
          // we've won
          io.emit('player_move', { pos: 9, msg: 'The AI Won Suckah!', state: gamestate, player: 'AI'});
          reset_game('The AI Won Suckah!');
        } else {
          if (ai_input === 9) {
            io.emit('player_move', { pos: 9, msg: 'DRAW', state: gamestate, player: 'AI'});
            reset_game('DRAW!');
          }
          
        }

      }
    } else {
    //  the move is illegal  
      io.emit('player_move', { pos: 10, msg: 'illegal manuever - please choose another position', state: gamestate, player: 'player'})
    }
    
  });
});

function reset_game(wintype){
  gamestate = [0,0,0,0,0,0,0,0,0];
  io.emit('player_move', { pos: 9, msg: wintype, state: gamestate, player: 'AI'});
}

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

function ai_turn(gamestate, input){

  //  If the AI can win, it should take it....

  // row 1 

  if (gamestate[0] === 2 && gamestate[1] === 2 && gamestate[2] === 0 ){
    return 2
  }
  else if (gamestate[0] === 2 && gamestate[2] === 2 && gamestate[1] === 0 ){
    return 1
  }
  else if (gamestate[1] === 2 && gamestate[2] === 2 && gamestate[0] === 0 ){
    return 0
  }

  // row 2 

  else if (gamestate[3] === 2 && gamestate[4] === 2 && gamestate[5] === 0 ){
    return 5
  }
  else if (gamestate[3] === 2 && gamestate[5] === 2 && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 2 && gamestate[5] === 2 && gamestate[3] === 0 ){
    return 3
  }

  // row 3 

  else if (gamestate[6] === 2 && gamestate[7] === 2 && gamestate[8] === 0 ){
    return 8
  }
  else if (gamestate[6] === 2 && gamestate[8] === 2 && gamestate[7] === 0 ){
    return 7
  }
  else if (gamestate[7] === 2 && gamestate[8] === 2 && gamestate[6] === 0 ){
    return 6
  }



  // 1 column
  else if (gamestate[0] === 2 && gamestate[3] === 2  && gamestate[6] === 0 ){
    return 6
  }
  else if (gamestate[0] === 2 && gamestate[6] === 2  && gamestate[3] === 0 ){
    return 3
  }
  else if (gamestate[3] === 2 && gamestate[6] === 2  && gamestate[0] === 0 ){
    return 0
  }

  // 2 column
  else if (gamestate[1] === 2 && gamestate[4] === 2  && gamestate[7] === 0 ){
    return 7
  }
  else if (gamestate[1] === 2 && gamestate[7] === 2  && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 2 && gamestate[7] === 2  && gamestate[1] === 0 ){
    return 1
  }

  // 3 column
  else if (gamestate[2] === 2 && gamestate[5] === 2  && gamestate[8] === 0 ){
    return 8
  }
  else if (gamestate[2] === 2 && gamestate[8] === 2  && gamestate[5] === 0 ){
    return 5
  }
  else if (gamestate[5] === 2 && gamestate[8] === 2  && gamestate[2] === 0 ){
    return 2
  }


  // diagonals backslash

  else if (gamestate[0] === 2 && gamestate[4] === 2 && gamestate[8] === 0 ){
    return 8
  }
  else if (gamestate[0] === 2 && gamestate[8] === 2  && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 2 && gamestate[8] === 2  && gamestate[0] === 0 ){
    return 0
  }


  // diagonals forwardslash

  else if (gamestate[2] === 2 && gamestate[4] === 2 && gamestate[6] === 0 ){
    return 6
  }
  else if (gamestate[2] === 2 && gamestate[6] === 2  && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 2 && gamestate[6] === 2  && gamestate[2] === 0 ){
    return 2
  }




//  If the player can win, it should stop it....



  // Mega Moves

  else if (gamestate[2] === 1 && gamestate[6] === 1  && gamestate[4] === 2 && gamestate[1] == 0 ){
    return 1
  }


  else if (gamestate[0] === 1 && gamestate[8] === 1  && gamestate[4] === 2 && gamestate[1] == 0 ){
    return 1
  }



  // row 1 

  else if (gamestate[0] === 1 && gamestate[1] === 1 && gamestate[2] === 0 ){
    return 2
  }
  else if (gamestate[0] === 1 && gamestate[2] === 1 && gamestate[1] === 0 ){
    return 1
  }
  else if (gamestate[1] === 1 && gamestate[2] === 1 && gamestate[0] === 0 ){
    return 0
  }

  // row 2 

  else if (gamestate[3] === 1 && gamestate[4] === 1 && gamestate[5] === 0 ){
    return 5
  }
  else if (gamestate[3] === 1 && gamestate[5] === 1 && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 1 && gamestate[5] === 1 && gamestate[3] === 0 ){
    return 3
  }

  // row 3 

  else if (gamestate[6] === 1 && gamestate[7] === 1 && gamestate[8] === 0 ){
    return 8
  }
  else if (gamestate[6] === 1 && gamestate[8] === 1 && gamestate[7] === 0 ){
    return 7
  }
  else if (gamestate[7] === 1 && gamestate[8] === 1 && gamestate[6] === 0 ){
    return 6
  }



  // 1 column
  else if (gamestate[0] === 1 && gamestate[3] === 1  && gamestate[6] === 0 ){
    return 6
  }
  else if (gamestate[0] === 1 && gamestate[6] === 1  && gamestate[3] === 0 ){
    return 3
  }
  else if (gamestate[3] === 1 && gamestate[6] === 1  && gamestate[0] === 0 ){
    return 0
  }

  // 2 column
  else if (gamestate[1] === 1 && gamestate[4] === 1  && gamestate[7] === 0 ){
    return 7
  }
  else if (gamestate[1] === 1 && gamestate[7] === 1  && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 1 && gamestate[7] === 1  && gamestate[1] === 0 ){
    return 1
  }

  // 3 column
  else if (gamestate[2] === 1 && gamestate[5] === 1  && gamestate[8] === 0 ){
    return 8
  }
  else if (gamestate[2] === 1 && gamestate[8] === 1  && gamestate[5] === 0 ){
    return 5
  }
  else if (gamestate[5] === 1 && gamestate[8] === 1  && gamestate[2] === 0 ){
    return 2
  }


  // diagonals backslash

  else if (gamestate[0] === 1 && gamestate[4] === 1 && gamestate[8] === 0 ){
    return 8
  }
  else if (gamestate[0] === 1 && gamestate[8] === 1  && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 1 && gamestate[8] === 1  && gamestate[0] === 0 ){
    return 0
  }


  // diagonals forwardslash

  else if (gamestate[2] === 1 && gamestate[4] === 1 && gamestate[6] === 0 ){
    return 6
  }
  else if (gamestate[2] === 1 && gamestate[6] === 1  && gamestate[4] === 0 ){
    return 4
  }
  else if (gamestate[4] === 1 && gamestate[6] === 1  && gamestate[2] === 0 ){
    return 2
  }





  //  There aren't two picks that threaten a line, 
  //  so pick the opposite of what was chosen or pick the middle square if it hasn't been picked yet

  else if (gamestate[4] === 0){
    return 4;
  }

  // 0
  else if(input == 0 && gamestate[8] === 0){
    return 8;
  }
  else if(input == 0 && gamestate[6] === 0){
    return 6;
  }
  else if(input == 0 && gamestate[2] === 0){
    return 2;
  }

  // 2
  else if(input == 2 && gamestate[0] === 0){
    return 0;
  }
  else if(input == 2 && gamestate[6] === 0){
    return 6;
  }
  else if(input == 2 && gamestate[8] === 0){
    return 8;
  }

  // 6
  else if(input == 6 && gamestate[2] === 0){
    return 2;
  }
  else if(input == 6 && gamestate[0] === 0){
    return 0;
  }
  else if(input == 6 && gamestate[8] === 0){
    return 8;
  }

  // 8
  else if(input == 8 && gamestate[0] === 0){
    return 0;
  }
  else if(input == 8 && gamestate[2] === 0){
    return 2;
  }
  else if(input == 8 && gamestate[6] === 0){
    return 6;
  }

  // The Player picked the middle

  else if(input == 4 && gamestate[0] === 0){
    return 0;
  }

  else if (gamestate[0] === 0){
    return 0
  }
  else if (gamestate[2] === 0){
    return 2
  }
  else if (gamestate[6] === 0){
    return 6
  }
  else if (gamestate[7] === 0){
    return 7
  }
  else if (gamestate[1] === 0){
    return 1
  }
  else if (gamestate[3] === 0){
    return 3
  }
  else if (gamestate[5] === 0){
    return 5
  }
  else if (gamestate[7] === 0){
    return 7
  }

  else {
    return 9
  }
}

http.listen(3000, function(){
  console.log('listening on *:3000');
});