<?php

/* NOTE:

	This can be shrunk down and cleaned up significantly from its current state. 
	I have started to write helper functions and move repeatable logic into it - however
	I wanted to get this working and submited sooner before interview on Wed.
	As I worked on this I realized better patterns and ideas on implementation- as common with most software problems.
	If needed I can refactor it further to show a more elegant solution.

	- Eugene K.
*/

include_once APP_DIR."/utils/http_utils.php";

class MakeMoveCommand
{
	function __construct()
	{
		//
	}
	
	function run($tictactoeMoves)
	{
		logInfo("Make move command called.");
		
		// respond to move one
		if(count($tictactoeMoves) == 1)
		{
			// respond to corner move
			if($this->isMoveInCorner($tictactoeMoves[0]))
			{
				array_push($tictactoeMoves, array(1, 1));
			}
			// respond to center edge move top-bottom
			if($this->isMoveInCenterOfTopBotEdge($tictactoeMoves[0]))
			{
				array_push($tictactoeMoves, array(1, 1));
			}
			// respond to center edge move left-right
			if($this->isMoveInCenterOfLeftRightEdge($tictactoeMoves[0]))
			{
				array_push($tictactoeMoves, array(1, 1));
			}
			// respond to center move
			if($this->isCenterMove($tictactoeMoves[0]))
			{
				array_push($tictactoeMoves, array(0, 0));
			}
		}

		// respond to move two
		if(count($tictactoeMoves) == 3)
		{
			if($this->isCenterMove($tictactoeMoves[1]))
			{
				// check if player moves share same edge of grid 
				if($tictactoeMoves[0][0] == 0 && $tictactoeMoves[2][0] == 0)
				{
					$tictactoeMoves = $this->blockEdgeWin($tictactoeMoves, 1, 0, NULL);
				}
				elseif($tictactoeMoves[0][0] == 2 && $tictactoeMoves[2][0] == 2)
				{
					$tictactoeMoves = $this->blockEdgeWin($tictactoeMoves, 1, 2, NULL);
				}
				elseif($tictactoeMoves[0][1] == 0 && $tictactoeMoves[2][1] == 0)
				{
					$tictactoeMoves = $this->blockEdgeWin($tictactoeMoves, 0, NULL, 0);
				}
				elseif($tictactoeMoves[0][1] == 2 && $tictactoeMoves[2][1] == 2)
				{
					$tictactoeMoves = $this->blockEdgeWin($tictactoeMoves, 0, null, 2);
				}
				// check if player has two diagonal corner moves
				elseif($this->areMovesOnDiagonalCorners($tictactoeMoves[0],$tictactoeMoves[2]))
				{
					array_push($tictactoeMoves, array(0,1));
				}
				// if the player's two moves are in a L-shape
				elseif($this->isMoveInCorner($tictactoeMoves[0]) || $this->isMoveInCorner($tictactoeMoves[2]))
				{
					if($this->isMoveInCorner($tictactoeMoves[0]))
					{
						if($tictactoeMoves[0][0] == 0)
						{
							array_push($tictactoeMoves, array(2,0));
						}
						else
						{
							array_push($tictactoeMoves, array(0,0));
						}
					}
					if($this->isMoveInCorner($tictactoeMoves[2]))
					{
						if($tictactoeMoves[2][0] == 0)
						{
							array_push($tictactoeMoves, array(2,0));
						}
						else
						{
							array_push($tictactoeMoves, array(0,0));
						}
					}
				}
				// if user made two center of edge moves, ai will just play diagnaly for the win
				else
				{
					array_push($tictactoeMoves, array(0,0));
				}
			}
			// if user made move on corner diagonal of ai move
			elseif ($this->areMovesOnDiagonalCorners($tictactoeMoves[1],$tictactoeMoves[2]))
			{
				array_push($tictactoeMoves, array(0,2));
			}
			elseif ($this->isMoveInCorner($tictactoeMoves[2]))
			{
				if($tictactoeMoves[2][0] == 0)
				{
					array_push($tictactoeMoves, array(2,0));
				}
				else
				{
					array_push($tictactoeMoves, array(0,2));
				}
			}
			elseif($this->isMoveInCenterOfTopBotEdge($tictactoeMoves[2]))
			{
				if($tictactoeMoves[2][0] == 0)
				{
					array_push($tictactoeMoves, array(2,1));
				}
				else
				{
					array_push($tictactoeMoves, array(0,1));
				}
			}
			elseif($this->isMoveInCenterOfLeftRightEdge($tictactoeMoves[2]))
			{
				if($tictactoeMoves[2][1] == 0)
				{
					array_push($tictactoeMoves, array(1,2));
				}
				else
				{
					array_push($tictactoeMoves, array(1,0));
				}
			}
		}

		// respond to move three
		if(count($tictactoeMoves) == 5)
		{
			// ai takes grid center as move one unless it is taken by the player first
			if($this->isCenterMove($tictactoeMoves[1]))
			{
				if($this->isMoveInCorner($tictactoeMoves[3]))
				{
					if($this->isCellEmpty($tictactoeMoves, $this->getDiagonalCellFromMove($tictactoeMoves[3])))
					{
						// AI wins
						array_push($tictactoeMoves, $this->getDiagonalCellFromMove($tictactoeMoves[3]));
					}
					elseif( ($this->isMoveInCorner($tictactoeMoves[0]) && $this->isMoveInCorner($tictactoeMoves[4])) &&
							(!$this->areMovesOnDiagonalCorners($tictactoeMoves[0], $tictactoeMoves[4])) &&
							($this->isCellEmpty($tictactoeMoves, array(0,1))) &&
							($this->isEdgeWinPossible(array($tictactoeMoves[0],$tictactoeMoves[2],$tictactoeMoves[4]))))
					{
						array_push($tictactoeMoves, array(0,1));
					}
					elseif($this->isMoveInCenterOfLeftRightEdge($tictactoeMoves[4]))
					{
						if($tictactoeMoves[4][1] == 2)
						{
							if($this->isCellEmpty($tictactoeMoves, array(2,2)))
							{
								array_push($tictactoeMoves, array(2,2));
							}
						}
					}
					elseif(count($this->getEmptyCornerCell($tictactoeMoves)) == 2)
					{
						array_push($tictactoeMoves, $this->getEmptyCornerCell($tictactoeMoves));
					}
				}
				elseif ($this->isMoveInCenterOfTopBotEdge($tictactoeMoves[3])) {
					if($this->isCellEmpty($tictactoeMoves, $this->getAccrossCellFromMove($tictactoeMoves[3])))
					{
						// AI wins
						array_push($tictactoeMoves, $this->getAccrossCellFromMove($tictactoeMoves[3]));
					}
					elseif(count($this->getEmptyCornerCell($tictactoeMoves)) == 2)
					{
						array_push($tictactoeMoves, $this->getEmptyCornerCell($tictactoeMoves));
					}
				}
				elseif ($this->isMoveInCenterOfLeftRightEdge($tictactoeMoves[3])) {
					if($this->isCellEmpty($tictactoeMoves, $this->getAccrossCellFromMove($tictactoeMoves[3])))
					{
						// AI wins
						array_push($tictactoeMoves, $this->getAccrossCellFromMove($tictactoeMoves[3]));
					}
				}
			}
			elseif ($this->isEdgeWinPossible(array($tictactoeMoves[1],$tictactoeMoves[3],array(3,3)))
					&& !$this->isMoveInCorner($tictactoeMoves[4])) {
				// AI wins
				if($tictactoeMoves[1][0] == $tictactoeMoves[3][0])
				{	//todo: clean up into helpers
					if($this->isCellEmpty($tictactoeMoves, array($tictactoeMoves[1][0], 0)))
					{
						array_push($tictactoeMoves, array($tictactoeMoves[1][0], 0));
					}
					elseif($this->isCellEmpty($tictactoeMoves, array($tictactoeMoves[1][0], 1)))
					{
						array_push($tictactoeMoves, array($tictactoeMoves[1][0], 1));
					}
					elseif($this->isCellEmpty($tictactoeMoves, array($tictactoeMoves[1][0], 2)))
					{
						array_push($tictactoeMoves, array($tictactoeMoves[1][0], 2));
					}
				}
				elseif($tictactoeMoves[1][1] == $tictactoeMoves[3][1])
				{
					if($this->isCellEmpty($tictactoeMoves, array(0, $tictactoeMoves[1][1])))
					{
						array_push($tictactoeMoves, array(0, $tictactoeMoves[1][1]));
					}
					elseif($this->isCellEmpty($tictactoeMoves, array(1, $tictactoeMoves[1][1])))
					{
						array_push($tictactoeMoves, array(1, $tictactoeMoves[1][1]));
					}
					elseif($this->isCellEmpty($tictactoeMoves, array(2, $tictactoeMoves[1][1])))
					{
						array_push($tictactoeMoves, array(2, $tictactoeMoves[1][1]));
					}
				}
			}
			elseif($this->isMoveInCorner($tictactoeMoves[4]) &&
				$this->isCellEmpty($tictactoeMoves, $this->getDiagonalCellFromMove($tictactoeMoves[4])))
			{
				array_push($tictactoeMoves, $this->getDiagonalCellFromMove($tictactoeMoves[4]));
			}
			elseif(count($this->getEmptyCornerCell($tictactoeMoves)) == 2)
			{
				array_push($tictactoeMoves, $this->getEmptyCornerCell($tictactoeMoves));
			}
		}

		// respond to move four
		if(count($tictactoeMoves) == 7)
		{
			if(count($this->getEmptyCornerCell($tictactoeMoves)) == 2)
			{
				array_push($tictactoeMoves, $this->getEmptyCornerCell($tictactoeMoves));
			}
			elseif(count($this->getEmptyEdgeCenterCell($tictactoeMoves)) == 2)
			{
				array_push($tictactoeMoves, $this->getEmptyEdgeCenterCell($tictactoeMoves));
			}
		}

		$result = $tictactoeMoves;

		return $result;
	}


// HELPERS

	function blockEdgeWin($tictactoeMoves, $coordinateIndex, $xAxisIndex, $yAxisIndex)
	{
		// todo: can add some error handling here
		if(($tictactoeMoves[0][$coordinateIndex] == 0 && $tictactoeMoves[2][$coordinateIndex] == 1) || ($tictactoeMoves[0][$coordinateIndex] == 1 && $tictactoeMoves[2][$coordinateIndex] == 0))
		{
			$axisIndex = 2;
		}
		elseif(($tictactoeMoves[0][$coordinateIndex] == 1 && $tictactoeMoves[2][$coordinateIndex] == 2) || ($tictactoeMoves[0][$coordinateIndex] == 2 && $tictactoeMoves[2][$coordinateIndex] == 1))
		{
			$axisIndex = 0;
		}
		else 
		{
			$axisIndex = 1;
		}

		if(!isset($yAxisIndex))
		{
			$yAxisIndex = $axisIndex;
		}

		if(!isset($xAxisIndex))
		{
			$xAxisIndex = $axisIndex;
		}

		array_push($tictactoeMoves, array($xAxisIndex, $yAxisIndex));

		return $tictactoeMoves;
	}

	function isMoveInCorner($move) 
	{
		if($move[0] == 0 || $move[0] == 2)
		{
			if($move[1] == 0 || $move[1] == 2)
			{
				return true;
			}
		}
		return false;
	}

	function areMovesOnDiagonalCorners($moveOne, $moveTwo)
	{
		if($this->isMoveInCorner($moveOne) && $this->isMoveInCorner($moveTwo))
		{
			if(($moveOne[0] != $moveTwo[0]) && ($moveOne[1] != $moveTwo[1]))
			{
				return true;
			}
			return false;
		}
		return false;
	}

	// todo: combine edge helpers
	function isMoveInCenterOfTopBotEdge($move) 
	{
		if($move[0] == 0 || $move[0] == 2)
		{
			if($move[1] == 1 || $move[1] == 1)
			{
				return true;
			}
		}
		return false;
	}

	function isMoveInCenterOfLeftRightEdge($move) 
	{
		if($move[0] == 1 || $move[0] == 1)
		{
			if($move[1] == 0 || $move[1] == 2)
			{
				return true;
			}
		}
		return false;
	}

	function isCenterMove($move) 
	{
		if($move[0] == 1 && $move[1] == 1)
		{
			return true;
		}
		return false;
	}

	function getEmptyCornerCell($moves)
	{
		if($this->isCellEmpty($moves, array(0,0)))
		{
			return array(0,0);
		}
		elseif($this->isCellEmpty($moves, array(0,2)))
		{
			return array(0,2);
		}
		elseif($this->isCellEmpty($moves, array(2,0)))
		{
			return array(2,0);
		}
		elseif($this->isCellEmpty($moves, array(2,2)))
		{
			return array(2,2);
		}
		else
		{
			return array();
		}
	}

	function getEmptyEdgeCenterCell($moves)
	{
		if($this->isCellEmpty($moves, array(0,1)))
		{
			return array(0,1);
		}
		elseif($this->isCellEmpty($moves, array(1,0)))
		{
			return array(1,0);
		}
		elseif($this->isCellEmpty($moves, array(1,2)))
		{
			return array(1,2);
		}
		elseif($this->isCellEmpty($moves, array(2,1)))
		{
			return array(2,1);
		}
		else
		{
			return array();
		}
	}
	function isCellEmpty($moves, $cell)
	{
		foreach($moves as $move) {
			if(($move[0] == $cell[0]) && ($move[1] == $cell[1]))
			{
				return false;
			}
		}
		return true;
	}

	function getDiagonalCellFromMove($move)
	{
		$xAxis = 0;
		$yAxis = 0;

		if($move[0] == 0)
		{
			$xAxis = 2;
		}
		if($move[1] == 0)
		{
			$yAxis = 2;
		}

		return array($xAxis, $yAxis);
	}

	function getAccrossCellFromMove($move)
	{
		$xAxis = $move[0];
		$yAxis = $move[1];

		if(($move[0] == 0) && ($move[1] == 1))
		{
			$xAxis = 2;
		}

		if(($move[0] == 2) && ($move[1] == 1))
		{
			$xAxis = 0;
		}

		if(($move[0] == 1) && ($move[1] == 0))
		{
			$yAxis = 2;
		}

		if(($move[0] == 1) && ($move[1] == 2))
		{
			$yAxis = 0;
		}

		return array($xAxis, $yAxis);
	}

	function isEdgeWinPossible($cells)
	{
		if(count($cells) == 3)
		{
			if(($cells[0][0] == $cells[1][0]) || ($cells[0][0] == $cells[2][0]) || ($cells[1][0] == $cells[2][0]))
			{
				return true;
			}
			elseif(($cells[0][1] == $cells[1][1]) || ($cells[0][1] == $cells[2][1]) || ($cells[1][0] == $cells[2][1]))
			{
				return true;
			}
		}
		
		return false;
	}

}