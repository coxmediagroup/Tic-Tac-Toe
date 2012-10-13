'use strict';
/* Memory Game Models and Business Logic */

function Tile(title) {
  this.title = title;
  this.flipped = false;
}

Tile.prototype.flip = function() {
  this.flipped = !this.flipped;
};



function Game(tileNames) {
  var tileDeck = makeDeck(tileNames);

  this.grid = makeGrid(tileDeck);
  this.message = Game.MESSAGE_CLICK;
  this.unmatchedPairs = tileNames.length;

  this.flipTile = function(tile) {
    if (tile.flipped) {
      return;
    }

    tile.flip();

    if (!this.firstPick || this.secondPick) {

      if (this.secondPick) {
        this.firstPick.flip();
        this.secondPick.flip();
        this.firstPick = this.secondPick = undefined;
      }

      this.firstPick = tile;
      this.message = Game.MESSAGE_ONE_MORE;

    } else {

      if (this.firstPick.title === tile.title) {
        this.unmatchedPairs--;
        this.message = (this.unmatchedPairs > 0) ? Game.MESSAGE_MATCH : Game.MESSAGE_WON;
        this.firstPick = this.secondPick = undefined;
      } else {
        this.secondPick = tile;
        this.message = Game.MESSAGE_MISS;
      }
    }
  }
}

Game.MESSAGE_CLICK = 'Click on a tile.';
Game.MESSAGE_ONE_MORE = 'Pick one more card.';
Game.MESSAGE_MISS = 'Try again.';
Game.MESSAGE_MATCH = 'Good job! Keep going.';
Game.MESSAGE_WON = 'You win!';



/* Create an array with two of each tileName in it */
function makeDeck(tileNames) {
  var tileDeck = [];
  tileNames.forEach(function(name) {
    tileDeck.push(new Tile(name));
    tileDeck.push(new Tile(name));
  });

  return tileDeck;
}


function makeGrid(tileDeck) {
  var gridDimension = Math.sqrt(tileDeck.length),
      grid = [];

  for (var row = 0; row < gridDimension; row++) {
    grid[row] = [];
    for (var col = 0; col < gridDimension; col++) {
        grid[row][col] = removeRandomTile(tileDeck);
    }
  }

  return grid;
}


function removeRandomTile(tileDeck) {
  var i = Math.floor(Math.random()*tileDeck.length);
  return tileDeck.splice(i, 1)[0];
}


function Human(marker){
    //Class for Human player
    var self = this;
    var init = function (){
        self.marker = marker;
        self.type = 'H';
        self.description = "Human";
    };

    function IsValidMove(userMove,gameInstance){
        return gameInstance.isValidMove(userMove);
    }

    var move = function(gameInstance){
         /*** Move are only from 0-8 ***/
        var mov = self.getValidMove(gameInstance);

        gameInstance.mark(self.marker,mov)
    };

    init();
}


function Computer(marker){
    var self = this;

    var init = function(){
        self.marker = marker;
        self.type = 'C';
        self.description = "Computer";
        if (self.marker === 'X'){
            self.opponent_marker = 'O';
        }
        else{
            self.opponent_marker = 'X';
        }
    };



    function move(gameInstance){
        var position_score = self.maximized_move(gameInstance),
            move_position = position_score['bestMove'];
        game_instance.mark(self.marker,move_position);
    }


    var maximized_move = function(game_instance){
        // Find maximized move
        var best_score, best_move, m,
            score, position_score;

        for (m in game_instance.get_free_positions()){
            game_instance.mark(self.marker,m);

            if (game_instance.is_game_over())
                score = self.get_score(game_instance);
            else
                position_score = self.minimized_move(game_instance);
                score = position_score['bestScore'];

            game_instance.revert_last_move();

            if ((best_score === undefined) || (score > best_score)){
                best_score = score;
                best_move = m;
            }
        }
        return { bestMove : best_move, bestScore : best_score };
    };

    var minimized_move = function(game_instance){
    //Find the minimized move
        var best_score, best_move, m,
            score, move_position_score;

        for (m in game_instance.get_free_positions()){
            game_instance.mark(self.opponent_marker,m)

            if (game_instance.is_game_over())
                score = self.get_score(game_instance);
            else {

                move_position_score = self.maximized_move(game_instance);
                score = move_position_score['bestScore'];
            }

            game_instance.revert_last_move();

            if ((best_score === undefined) || (score < best_score)){
                best_score = score;
                best_move = m;
            }
        }

        return { bestMove : best_move, bestScore : best_score };
    };

    var get_score = function(game_instance){
        if (game_instance.is_game_over())
            if ((game_instance.winner  === self.marker))
                return 1; // Won
            else if (game_instance.winner === self.opponent_marker)
                return -1; // Opponent won
        return 0; // Draw
    }

    init();
}

function Game(){

    var init = function(){
        //Initialize parameters - the game board, moves stack and winner

        self.board = ['-', '-', '-', '-', '-', '-', '-', '-', '-'];
        self.last_moves = [];
        self.winner = undefined;
    };


     function get_free_positions(){
        //Get the list of available positions
        var i, moves = [];
        for (i = 0; i < 9; i+=1){
            if (self.board[i] === '-'){
                moves.push(i);
            }
        }
        return moves;
     }

     function mark(marker,pos){
        //Mark a position with marker X or O
        self.board[pos] = marker;
        self.last_moves.push(pos);
     }

    function revert_last_move(){
        ///Reset the last move
        self.board[self.last_moves.pop()] = '-';
        self.winner = undefined;
    }

    var hm_possible_plays = function(){
        var plays = self.board.filter(
            function (item) {
                return item === '-';
            }
        );
        return plays.length;
    };

    function is_game_over(){
    //    Test whether game has ended

        var i, win_position, state,
            win_positions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6],[1,4,7],[2,5,8], [0,4,8], [2,4,6]],
            len_win_positions = win_positions.length;

        for (i = 0; i < len_win_positions; i += 1){
            win_position = win_positions[i];
            state = win_position.map(function (item) { return self.board[item]; });
            if ((state[0] === state[1]) && (state[1] === state[2]) && (state[0] != '-'))
                self.winner = self.state[0];
            return true;
        }
        if (hm_possible_plays() === 0){
            self.winner = '-';
            return true;
        }
        else
            return false;
    }
    var display_who_is_playing = function(player){
        if (player.type === 'H')
            console.log("\t\t[Human's Move]");
        else
            console.log("\t\t[Computer's Move]");
    };

    function play(player1,player2){
        //Execute the game play with players
        var i, current_player;

        self.p1 = player1;
        self.p2 = player2;


        for (i = 0; i < 9; i+=1){

            if (i%2==0){
                current_player = self.p1;
                display_who_is_playing(current_player);
                self.p1.move(self);
            }
            else{
                current_player = self.p2;
                display_who_is_playing(current_player);
                self.p2.move(self);
            }

            if (self.is_game_over()){
                if (self.winner === '-')
                    console.log("\nGame over with Draw");
                else
                    console.log("\n" + current_player.description+ " wins ");
                return;
            }
        }
    }

    init();
}

