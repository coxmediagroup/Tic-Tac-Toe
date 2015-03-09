<?php

    /**
    * TicTacToe Game. 
    * @author Eric Blanks
    */

	class TicTacToe {

		private $currentPlayer = 'o';
		private $board;
		private $winner;
        private $player1Wins = 0;
        private $player2Wins = 0;
        private $drawWins = 0;
        private $winData;

		public function __construct() {
        }

        // Sets board back to empty
		
    	public function newGame() {

            for($x = 0; $x < 3; $x++) {
            	for($y = 0; $y < 3; $y ++) {
            		$this->board[$x][$y] = '-';
            	}
            }

            $this->currentPlayer = 'o';
    	}

        /**
         *  Sets player 1 move
         *  @param $x position, $y position, $setBlank set pos to blank
         *  @returns results 
         */
    	public function userMove($x, $y, $setBlank=false) {
    		
            if($setBlank) {
                $this->board[$x][$y] = '-';
            } else {
                $this->board[$x][$y] = $this->currentPlayer;
            }
    		  
    		$results['currentPlayer'] = $this->currentPlayer;
            $results = $this->handleResults($results);

    		return $results;
    	}

        /**
         *  Sets player 2 move via best position (min max algo)
         *  @returns results 
         */

    	public function computerMove() {
            
			$results['currentPlayer'] = $this->currentPlayer;
    		$move = $this->minMax();
            
            $this->board[$move[0]][$move[1]] = $this->currentPlayer;
    		$results['computerMove'] = $move[0] . '_' .$move[1];
            $results = $this->handleResults($results);
           
    		return $results;
    	}

        /**
         *  results of move
         *  @returns results 
         */

        private function handleResults($results) {
            $winner = $this->isGameOver();
            $results['winner'] = $winner;

            if($winer ===  'x') {
                $this->player1Wins++;
            } else if ($winner === 'o') {
                $this->player2Wins++;
            } else if ($winner === 'c') {
                $this->drawWins++;
            }

            $results['stats'] = array('player1Wins' => $this->player1Wins, 
                'player2Wins' => $this->player2Wins,
                'drawWins' => $this->drawWins);

            if($winner == 'x' || $winner == 'o') {
                $results['winData'] = $this->winData;
            }

            return $results;
        }

    	// returns best move for the current computer player
    	private function minMax() {

            $game = clone $this;
            $gameBoard = $game->getGameBoard();
    		$best = -10000;

    		for($x = 0; $x < 3; $x++) {
    			for($y = 0; $y < 3; $y++) {

    				if($gameBoard[$x][$y] != '-') {

    					continue;
    				}
    				$gameClone = clone $this;
    				$gameClone->userMove($x, $y);
    				$gameClone->changePlayer();
    				$value = $this->minMove($gameClone, 1, $best, 10000);
                    $gameClone->userMove($x, $y, true);


    				if($value > $best) {
    					$best = $value;
    					$move = array($x, $y);
    				}
                    $gameClone->changePlayer();
    			}
    		}

    		if(!empty($move)) {
    			return $move;
    		} 
    	}

    	public function getGameBoard() {
    		return $this->board;
    	}

        /**
         *  isAvailableSpace
         *  @return true if more moves false otherwise
         */
    	private function isAvailableSpace() {
    		for($x = 0; $x < 3; $x++) {
    			for($y = 0; $y < 3; $y++) {
    				if($this->board[$x][$y] == '-') {
    					return true;
    				}
    			}
    		}

            return false;
    	}

        /**
         *  Check if the game is over: 
         *      1. check if we have full row 
         *      2. check if we have full column 
         *      3. check if we have diagonal 
         *      4. its a draw? 
         *      5. game isn't over 
         *  @returns x for x winner, o for o winner, c for draw and - for none
         */
        public function isGameOver(){ 

            //FULL ROW 
            for($i=0; $i<3;$i++){
                if (false !== $this->board[$i][0] &&($this->board[$i][0] == $this->board[$i][1]
                    && $this->board[$i][1] == $this->board[$i][2])){ 
                    $this->winData = array("row" => $i);
                    return $this->board[$i][0]; 
                } 
            } 
            
            //FULL COLUMN
            for($i=0; $i<3;$i++){
                if (false !== $this->board[0][$i] &&($this->board[0][$i] == $this->board[1][$i]
                    && $this->board[1][$i] == $this->board[2][$i])){ 
                    $this->winData = array("col" => $i);
                    return $this->board[0][$i]; 
                } 
            } 
            
            //DIAGONAL
            $diagnolWon = false; 
            if (($this->board[0][0] == $this->board[1][1] 
                    && $this->board[1][1] == $this->board[2][2])) {
                $this->winData = array("diagnol1" => "diagnol1");
                $diagnolWon = true;
            } else if (($this->board[0][2] == $this->board[1][1]
                    && $this->board[1][1] == $this->board[2][0])){
                $this->winData = array("diagnol2" => "diagnol2");
                $diagnolWon = true;
            }        
            if ($diagnolWon && '-' !== $this->board[1][1]){ 
                    return $this->board[1][1]; 
            }
            
            //DRAW
            if (!$this->isAvailableSpace()) {
                return 'c'; 
            }
            
            //GAME IS ON
            return '-';
        } 


        /**
         *  Get current node score 
         *  @param Game 
         *  @param int  $depth
         *  @returns score
        */
    	private function score($game, $depth) {
            $res = $game->isGameOver();
  
    		switch($res) {
    			case 'x':
    				return $depth - 100;
    				break;
    			case 'o':
    				return 100 - $depth;
    			case 'c':
    				return  0;
    			default :
    				return 1;
    		}
    	}

        /**
         *  Apply Max Moves 
         *  @param Game $gameClone
         *  @param int $depth
         *  @param int $alpha
         *  @param int $beta
            @returns int
        */

    	private function maxMoves($gameClone, $depth, $alpha, $beta) {
        
    		$res = $this->score($gameClone, $depth);
    		if($res != 1) {
    			return $res;
    		}

    		$gameBoard = $gameClone->getGameBoard();

    		for($x = 0; $x < 3; $x++) {
    			for($y = 0; $y < 3; $y++) {
    				if($gameBoard[$x][$y] != '-') {
    					continue;
    				}

    				$gameClone->userMove($x, $y);
    				$gameClone->changePlayer();
    				$value = $this->minMove($gameClone, ++$depth, $alpha, $beta);

                    $gameClone->userMove($x, $y, true);
                    $gameClone->changePlayer();

                    if($value > $alpha) {
                        $alpha = $value;
                    }

                    if($alpha > $beta) {
                        return $beta;
                    }			
    			}
    		}

    		return $value;
    	}

        /* computes the minimal move based on the minmax algorithm 
        *  @param Game $gameClone
        *  @param int $depth
        *  @param int $alpha
        *  @param int $beta
        *  @returns int
        */

    	private function minMove($gameClone, $depth, $alpha, $beta) {
    		$res = $this->score($gameClone, $depth);

    		if($res != 1) {
    			return $res;
    		}

    		$gameBoard = $gameClone->getGameBoard();

    		for($x = 0; $x < 3; $x++) {
    			for($y = 0; $y < 3; $y++) {
    				if($gameBoard[$x][$y] != '-') {
    					continue;
    				}
					$gameClone->userMove($x, $y);
					$gameClone->changePlayer();
					$value = $this->maxMoves($gameClone, ++$depth, $alpha, $beta);
                    $gameClone->userMove($x, $y, true);
                    $gameClone->changePlayer();
                    if($value <  $beta) {
                        $beta = $value;
                    }

                    if($beta < $alpha) {
                        return $alpha;
                    }
                
    			}
    		}
    		return $value;
    	}

    	// Change player marks back and forth.
	    public function changePlayer() {

	        if ($this->currentPlayer == 'x') {
	            $this->currentPlayer = 'o';
	        }
	        else {
	            $this->currentPlayer = 'x';
	        }
	    }
	}
?>