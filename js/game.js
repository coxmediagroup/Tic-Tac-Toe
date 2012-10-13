'use strict';
/* Memory Game Models and Business Logic */





function Human(marker){
    //Class for Human player
    var self = this;
    var init = function (){
        self.marker = marker;
        self.type = 'H';
        self.description = "Human";
    };

    self.IsValidMove = function (userMove,gameInstance){
        return gameInstance.isValidMove(userMove);
    };

    self.move = function(gameInstance, mov){
         /*** Move are only from 0-8 ***/
        //var mov = self.getValidMove(gameInstance);
        gameInstance.mark(self.marker,mov)
    };

    init();
    return self;
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


    self.move = function (gameInstance){
        var position_score = maximized_move(gameInstance),
            move_position = position_score['bestMove'];
        gameInstance.mark(self.marker,move_position);
    };


    var maximized_move = function(gameInstance){
        // Find maximized move
        var best_score, best_move, i, m,
            score, position_score,
            free_positions = gameInstance.get_free_positions(),
            len_free_positions = free_positions.length;

        for (i = 0; i < len_free_positions; i += 1){
            m = free_positions[i];
            gameInstance.mark(self.marker,m);

            if (gameInstance.is_game_over())
                score = get_score(gameInstance);
            else{
                position_score = minimized_move(gameInstance);
                score = position_score['bestScore'];
            }

            gameInstance.revert_last_move();

            if ((best_score === undefined) || (score > best_score)){
                best_score = score;
                best_move = m;
            }
        }
        return { bestMove : best_move, bestScore : best_score };
    };

    var minimized_move = function(gameInstance){
    //Find the minimized move
        var best_score, best_move, i, m,
            score, move_position_score,
            free_positions = gameInstance.get_free_positions(),
            len_free_positions = free_positions.length;

        for (i = 0; i < len_free_positions; i += 1){
            m = free_positions[i];

            gameInstance.mark(self.opponent_marker,m);

            if (gameInstance.is_game_over())
                score = get_score(gameInstance);
            else {
                move_position_score = maximized_move(gameInstance);
                score = move_position_score['bestScore'];
            }

            gameInstance.revert_last_move();

            if ((best_score === undefined) || (score < best_score)){
                best_score = score;
                best_move = m;
            }
        }

        return { bestMove : best_move, bestScore : best_score };
    };

    var get_score = function(gameInstance){
        if (gameInstance.is_game_over())
            if ((gameInstance.winner  === self.marker))
                return 1; // Won
            else if (gameInstance.winner === self.opponent_marker)
                return -1; // Opponent won
        return 0; // Draw
    };

    init();
    return self;
}

function Game(){
    var self = this;

    var initializeMessages = function () {
        self.MESSAGE_HUMAN_TURN = 'Your turn.';
        self.MESSAGE_COMPUTER_TURN = "Computer's turn";
        self.MESSAGE_MISS = 'Computer won... Try again.';
        self.MESSAGE_WON = 'You won!';
    };

    self.initialize = function(){
        //Initialize parameters - the game board, moves stack and winner

        self.board = ['-', '-', '-', '-', '-', '-', '-', '-', '-'];
        self.last_moves = [];
        self.winner = undefined;

        initializeMessages();
    };

     self.get_free_positions = function (){
        //Get the list of available positions
        var i, moves = [];
        for (i = 0; i < 9; i+=1){
            if (self.board[i] === '-'){
                moves.push(i);
            }
        }
        return moves;
     };

    self.mark = function (marker,pos){
        //Mark a position with marker X or O
        self.board[pos] = marker;
        self.last_moves.push(pos);
     };

    self.revert_last_move = function (){
        ///Reset the last move
        self.board[self.last_moves.pop()] = '-';
        self.winner = undefined;
    };

    var hm_possible_plays = function(){
        var plays = self.board.filter(
            function (item) {
                return item === '-';
            }
        );
        return plays.length;
    };

    var get_state = function(win_position){
        return win_position.map(function (item) { return self.board[item]; });
    };

    self.is_game_over = function (){
    //    Test whether game has ended

        var i, win_position, state,
            win_positions = [[0,1,2], [3,4,5], [6,7,8], [0,3,6],[1,4,7],[2,5,8], [0,4,8], [2,4,6]],
            len_win_positions = win_positions.length;

        for (i = 0; i < len_win_positions; i += 1){
            win_position = win_positions[i];
            state = get_state(win_position);
            if ((state[0] === state[1]) && (state[1] === state[2]) && (state[0] != '-')){
                self.winner = state[0];
                return true;
            }
        }
        if (hm_possible_plays() === 0){
            self.winner = '-';
            return true;
        }
        else
            return false;
    };

    var display_who_is_playing = function(player){
        if (player.type === 'H')
            console.log("\t\t[Human's Move]");
        else
            console.log("\t\t[Computer's Move]");
    };

    self.play = function (player1,player2){
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
    };

    self.isValidMove = function (move){
        var positions = self.get_free_positions(),
            result = positions.filter(function (item){return item === move });

        return result.length === 1;
    };

    self.value = function(position){
        var trans = {
            'X' : " X ",
            'O' : " O ",
            '-' : "   "
           };
        return trans[self.board[position]];
    };

    self.initialize();
    return self;
}




