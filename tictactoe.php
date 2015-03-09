<?php

	class TicTacToe {

		private $numMoves = 0;
		private $currentPlayer = 'o';
		private $count = 0;
		private $board;
		private $winner;

		public function __construct() {

        }
		
    	public function newGame() {

            for($x = 0; $x < 3; $x++) {
            	for($y = 0; $y < 3; $y ++) {
            		$this->board[$x][$y] = '-';
            	}
            }

            $this->currentPlayer = 'o';
            $this->numMoves = 0;
            $results['board'] = $this->board;
            return $results;
    	}

    	public function userMove($position, $setBlank=false) {
    		$this->numMoves += 1;
    		$x = substr($position, 0, 1);
    		$y = substr($position, 2, 1);

            if($setBlank) {

                $this->board[$x][$y] = '-';
            } else {
                $this->board[$x][$y] = $this->currentPlayer;
            }
    		  
    		$results['currentPlayer'] = $this->currentPlayer;

            $winner = $this->isGameOver();
            $results['winner'] = $winner;

            /*
    		if($this->checkForWin()) {
    			$this->winner = $this->currentPlayer;
    			$results['winner'] = $this->winner;
    		}
    		else if(!$this->isAvailableSpace()) {
    			$this->winner = 'c';
    			$results['winner'] = $this->winner; // cat
    		} 
            */

            

    		$results['board'] = $this->board;
            $results['numMoves'] = $this->numMoves;

    		return $results;
    	}


    	public function getWinner() {
    		return $this->winner;
    	}

    	public function computerMove() {

            $this->numMoves += 1;
            
            
			$results['currentPlayer'] = $this->currentPlayer;
    		$move = $this->minMax();
            $x = substr($move, 0, 1);
            $y = substr($move, 2, 1);
            $this->board[$x][$y] = $this->currentPlayer;
    		$results['computerMove'] = $move;
    		$results['debug'] = $this->debug;

            /*

            if($this->checkForWin()) {
                $this->winner = $this->currentPlayer;
                $results['winner'] = $this->winner;
            }
            else if(!$this->isAvailableSpace()) {
                $this->winner = 'c';
                $results['winner'] = $this->winner; // cat
            } 

            */

            $winner = $this->isGameOver();
            $results['winner'] = $winner;

            $results['board'] = $this->board;
            $results['numMoves'] = $this->numMoves;

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
    				$gameClone->userMove($x . '_' . $y);
    				$gameClone->changePlayer();
    				$value = $this->minMove($gameClone, 1, $best, 10000);
                    $gameClone->userMove($x . '_' . $y, true);


    				if($value > $best) {
    					$best = $value;
    					$move = $x . "_" . $y;
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

        public function isGameOver(){ 

        //FULL ROW 
        for($i=0; $i<3;$i++){
            if (false !== $this->board[$i][0] &&($this->board[$i][0] == $this->board[$i][1]
                && $this->board[$i][1] == $this->board[$i][2])){ 
                return $this->board[$i][0]; 
            } 
        } 
        
        //FULL COLUMN
        for($i=0; $i<3;$i++){
            if (false !== $this->board[0][$i] &&($this->board[0][$i] == $this->board[1][$i]
                && $this->board[1][$i] == $this->board[2][$i])){ 
                return $this->board[0][$i]; 
            } 
        } 
        
        //DIAGONAL 
        if (($this->board[0][0] == $this->board[1][1] 
                && $this->board[1][1] == $this->board[2][2]) 
                || ($this->board[0][2] == $this->board[1][1]
                && $this->board[1][1] == $this->board[2][0])){
                
            if (false !== $this->board[1][1]){ 
                return $this->board[1][1]; 
            } 
        }
        
        
        //DRAW
        if (!$this->isAvailableSpace()) {
            return 'c'; 
        }
        
        //GAME IS ON
        return '-';
    } 
/*
        private function score($game, $depth) {
            switch($game->getWinner()) {
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

    				$gameClone->userMove($x . '_' . $y);
    				$gameClone->changePlayer();
    				$value = $this->minMove($gameClone, ++$depth, $alpha, $beta);

                    $gameClone->userMove($x . '_' . $y, true);
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
					$gameClone->userMove($x . '_' . $y);
					$gameClone->changePlayer();
					$value = $this->maxMoves($gameClone, ++$depth, $alpha, $beta);
                    $gameClone->userMove($x . '_' . $y, true);
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

    	private function getAvailableMoves($board, $player) {

    		$availableMoves = array(array());
    		$i = 0;
    		for($x = 0; $x < 3; $x++) {
            	for($y = 0; $y < 3; $y ++) {
            		if($board[$x][$y] == '-') {
            			$availableMoves[$i] = array($x, $y);
            			$i++;
            		}
            	}
            }
            return $availableMoves;

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

    	// This calls our other win check functions to check the entire board.
    	private function checkForWin() {
        	return ($this->checkRowsForWin() || $this->checkColumnsForWin() || $this->checkDiagonalsForWin());
    	}

    	// Loop through rows and see if any are winners.
    	private function checkRowsForWin() {
	        for ($i = 0; $i < 3; $i++) {
	            if ($this->checkRowCol($this->board[$i][0], $this->board[$i][1], $this->board[$i][2]) == true) {
	                return true;
	            }
	        }
	        return false;
    	}


    	// Loop through columns and see if any are winners.
    	private function checkColumnsForWin() {
	        for ($i = 0; $i < 3; $i++) {
	            if ($this->checkRowCol($this->board[0][$i], $this->board[1][$i], $this->board[2][$i]) == true) {
	                return true;
	            }
	        }
        	return false;
    	}

    	// Check the two diagonals to see if either is a win. Return true if either wins.
	    private function checkDiagonalsForWin() {
	        return (($this->checkRowCol($this->board[0][0], $this->board[1][1], $this->board[2][2]) == true) || 
	        	($this->checkRowCol($this->board[0][2], $this->board[1][1], $this->board[2][0]) == true));
	    }

	    // Check to see if all three values are the same (and not empty) indicating a win.
	    private function checkRowCol($c1, $c2, $c3) {
	        return ((strcmp($c1, '-') != 0 ) && (strcmp($c1, $c2) == 0) && (strcmp($c2, $c3) ==0));
	    }
	}
?>