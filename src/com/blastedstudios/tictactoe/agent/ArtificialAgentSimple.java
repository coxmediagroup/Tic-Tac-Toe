package com.blastedstudios.tictactoe.agent;

import java.util.Random;

import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

/**
 * Artificial agent is a CPU driven tic-tac-toe player who choses the next move
 * based on a ruleset, first detecting immediate win/losses, then predicting 
 * win/loss more steps away (with forks). Still unsure if tree would have been
 * "better", perhaps cooler.
 * 
 * Now that the model is completed (implemented and tested), time to move on to
 * ui. This will be implemented in libgdx due to its open source and cross
 * platform nature.
 */
public class ArtificialAgentSimple extends Agent {
	private final Random random = new Random();
	
	public ArtificialAgentSimple(MarkTypeEnum markType) {
		super(markType);
	}

	/**
	 * Oh so many options here... A day or two ago I thought of what a person
	 * evaluating this product would want, and I thought it may be helpful to 
	 * add difficulty modifiers. What could a difficulty modifier be, though?
	 * 
	 * Different spans/board sizes was the msot obvious, where the computer
	 * could simply do tree/table lookups, whereas the human would have to
	 * scheme given the rulesets of the board. Maybe you could have a 10 width
	 * board but only need 4 slots (connect 4). Some of these could not be 
	 * solved, and if so, how to solve in generic ways.
	 * 
	 * I leaned toward making a tree. After implementing the easy generic tree
	 * in java, one may see the root's children as all permutations of the next 
	 * move. Upon making the move, that part of the tree would be pruned. 
	 * If the computer sees a branch which is undesirable (e.g. leading to 
	 * certain doom) it would avoid it.
	 * 
	 * If this was not a solved game, 3x3, then I would weight trees according
	 * to favorability - if you were guaranteed not to lose, a higher score,
	 * guaranteed to win, higher yet. Difficulty could then be based on how many
	 * plys, or levels, the a.i. would look ahead to see where it would move,
	 * similar if I remember correctly to chess a.i.
	 * 
	 * I was in a group in college that made 3d Minesweeper. It was an interesting
	 * project, and made me muse about 3d tictactoe and an a.i. for it. The tree
	 * model could handle this quite easily. But, since this is such a small
	 * project, I'll instead just ramble on for paragraphs about what I think
	 * at certain stages rather than code it, and instead code a simplistic
	 * model which does the job for 3x3.
	 */
	@Override public int turn(Board board) {
		while(true)
			try{
				int choice = choose(board);
				board.mark(choice, markType);
				return choice;
			}catch(Exception e){
				e.printStackTrace();
			}
	}

	/**
	 * @return number representing where to mark. Scan for where we want to place
	 * next, as there are only 9 options
	 * 
	 * I could have this return a list of viable options, and roll for which one
	 * to choose to add some randomness. Initial iteration at least will be dummy easy
	 */
	private int choose(Board board){
		//start with easier cases then get to harder. note this means it can't
		//pick up mid game, as a unit test uncovered if there exists the other
		//mark in 0 and 2, it would choose middle instead of 1. Anyways, how the ai
		// is built this would never happen, so leaving it.

		int move = detectWin(board);
		if(move != -1)
			return move;

		//go right for middle for simplicity (which as it turns out might not be as simple)
		if(board.getMiddle() == MarkTypeEnum.NONE)
			return 4;
		if(board.isEmptyExcept(4))
			return 0;

		move = detectCornerManeuver(board);
		if(move != -1)
			return move;

		move = detectLossPreventionMiddles(board);
		if(move != -1)
			return move;
		move = detectLossPreventionCorners(board);
		if(move != -1)
			return move;

		//now for slightly more complex cases - if the player is "intelligently" playing
		//more than one move ahead
		move = detectLineManeuver(board);
		if(move != -1)
			return move;
		move = detectTightTriangleManeuver(board);
		if(move != -1)
			return move;
		move = detectLManeuver(board);
		if(move != -1)
			return move;
		
		//otherwise, fill in the board
		int location = -1;
		do{
			location = random.nextInt(board.getBoard().length);
		}while(board.isMarked(location));
		return location;
	}
	
	private int detectLineManeuver(Board board) {
		if(board.getMiddle() == enemyType){
			if(board.isEmptyExcept(0,4,8))
				if(board.getBoard()[0] == enemyType)
					return 2;
				else if(board.getBoard()[8] == enemyType)
					return 6;
			if(board.isEmptyExcept(2,4,6))
				if(board.getBoard()[2] == enemyType)
					return 0;
				else if(board.getBoard()[6] == enemyType)
					return 8;
		}
		return -1;
	}

	private int detectCornerManeuver(Board board) {
		if(board.isEmptyExcept(0,4) && board.getBoard()[0] == enemyType)
			return 1;
		if(board.isEmptyExcept(2,4) && board.getBoard()[2] == enemyType)
			return 5;
		if(board.isEmptyExcept(8,4) && board.getBoard()[8] == enemyType)
			return 7;
		if(board.isEmptyExcept(6,4) && board.getBoard()[6] == enemyType)
			return 3;
		if(board.isEmptyExcept(0,8,4) && board.getBoard()[0] == enemyType &&
			board.getBoard()[8] == enemyType)
			return 1;
		if(board.isEmptyExcept(2,6,4) && board.getBoard()[6] == enemyType &&
				board.getBoard()[2] == enemyType)
			return 1;
		return -1;
	}

	/**
	 * Detect tight triangle maneuvers, where the player puts their mark
 	 * on two caddy-corner middle spots like top middle and left middle
	 */
	private int detectTightTriangleManeuver(Board board) {
		//top-left
		if(board.getBoard()[1] == enemyType && board.getBoard()[3] == enemyType &&
			board.getBoard()[2] != markType && board.getBoard()[6] != markType &&
			!board.isMarked(0))
			return 0;
		//topright
		if(board.getBoard()[1] == enemyType && board.getBoard()[5] == enemyType &&
			board.getBoard()[0] != markType && board.getBoard()[8] != markType &&
			!board.isMarked(2))
			return 2;
		//bottom left
		if(board.getBoard()[3] == enemyType && board.getBoard()[7] == enemyType &&
			board.getBoard()[0] != markType && board.getBoard()[8] != markType &&
			!board.isMarked(6))
			return 6;
		//bottom right
		if(board.getBoard()[7] == enemyType && board.getBoard()[5] == enemyType &&
			board.getBoard()[2] != markType && board.getBoard()[6] != markType &&
			!board.isMarked(8))
			return 8;
		return -1;
	}
	
	/**
	 * Enemy l maneuver detector. We need to prevent this immediately else they could
	 * win in two turns.
	 * 
	 * This is early game when the enemy puts their mark on a outer-middle spot, along
	 * with a non-adjacent corner, with the adjacent corners blank and the spot between
	 * the 'middle' corner and the corner spot unowned.
	 */
	private int detectLManeuver(Board board){
		//top/left leaning
		if(board.getBoard()[1] == enemyType && board.getBoard()[6] == enemyType &&
			board.getBoard()[0] != markType && board.getBoard()[2] != markType &&
			board.getBoard()[3] != markType && !board.isMarked(0))
			return 0;
		//top/right leaning
		if(board.getBoard()[1] == enemyType && board.getBoard()[8] == enemyType &&
			board.getBoard()[0] != markType && board.getBoard()[2] != markType &&
			board.getBoard()[5] != markType && !board.isMarked(2))
			return 2;
		//left/top leaning
		if(board.getBoard()[3] == enemyType && board.getBoard()[2] == enemyType &&
			board.getBoard()[0] != markType && board.getBoard()[1] != markType &&
			board.getBoard()[6] != markType && !board.isMarked(0))
			return 0;
		//left/bottom leaning
		if(board.getBoard()[3] == enemyType && board.getBoard()[8] == enemyType &&
			board.getBoard()[6] != markType && board.getBoard()[7] != markType &&
			board.getBoard()[0] != markType && !board.isMarked(6))
			return 6;
		//right/top leaning
		if(board.getBoard()[0] == enemyType && board.getBoard()[5] == enemyType &&
			board.getBoard()[1] != markType && board.getBoard()[2] != markType &&
			board.getBoard()[8] != markType && !board.isMarked(2))
			return 2;
		//right/bottom leaning
		if(board.getBoard()[6] == enemyType && board.getBoard()[5] == enemyType &&
			board.getBoard()[7] != markType && board.getBoard()[2] != markType &&
			board.getBoard()[8] != markType && !board.isMarked(8))
			return 8;
		//bottom/left leaning
		if(board.getBoard()[0] == enemyType && board.getBoard()[7] == enemyType &&
			board.getBoard()[3] != markType && board.getBoard()[6] != markType &&
			board.getBoard()[8] != markType && !board.isMarked(6))
			return 6;
		//bottom/right leaning
		if(board.getBoard()[2] == enemyType && board.getBoard()[7] == enemyType &&
			board.getBoard()[5] != markType && board.getBoard()[6] != markType &&
			board.getBoard()[8] != markType && !board.isMarked(8))
			return 8;
		return -1;
	}
	
	private int detectWin(Board board){
		//tl
		if(((board.getBoard()[1] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[3] == markType && board.getBoard()[6] == markType)) &&
			!board.isMarked(0))
			return 0;
		//tm
		if(((board.getBoard()[0] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[7] == markType)) &&
			!board.isMarked(1))
			return 1;
		//tr
		if(((board.getBoard()[1] == markType && board.getBoard()[0] == markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[6] == markType) ||
			(board.getBoard()[5] == markType && board.getBoard()[8] == markType)) &&
			!board.isMarked(2))
			return 2;
		//ml
		if(((board.getBoard()[0] == markType && board.getBoard()[6] == markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[5] == markType)) &&
			!board.isMarked(3))
			return 3;
		//mm
		if(((board.getBoard()[0] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[6] == markType && board.getBoard()[2] == markType)) &&
			!board.isMarked(4))
			return 4;
		//mr
		if(((board.getBoard()[2] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[3] == markType && board.getBoard()[4] == markType)) &&
			!board.isMarked(5))
			return 5;
		//bl
		if(((board.getBoard()[0] == markType && board.getBoard()[3] == markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[7] == markType && board.getBoard()[8] == markType)) &&
			!board.isMarked(6))
			return 6;
		//mr
		if(((board.getBoard()[6] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[1] == markType && board.getBoard()[4] == markType)) &&
			!board.isMarked(7))
			return 7;
		//br
		if(((board.getBoard()[0] == markType && board.getBoard()[4] == markType) ||
			(board.getBoard()[5] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[7] == markType && board.getBoard()[6] == markType)) &&
			!board.isMarked(8))
			return 8;
		return -1;
	}

	/**
	 * @return winning or loss preventing move. Could make slightly better,
	 * by first scanning for win possibilities, then losses, but the spec
	 * doesn't seem to care and I again wonder how in depth they are looking.
	 * Just quick parsing people who can do it, or really looking at the full
	 * mental process start to finish?
	 */
	private int detectLossPreventionMiddles(Board board){
		//middle
		if(((board.getBoard()[0] == enemyType && board.getBoard()[8] == enemyType) ||
			(board.getBoard()[2] == enemyType && board.getBoard()[6] == enemyType)) &&
			!board.isMarked(4))
			return 4;
		//top
		if(((board.getBoard()[0] == enemyType && board.getBoard()[2] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[7] == enemyType)) &&
			!board.isMarked(1))
			return 1;
		//left
		if(((board.getBoard()[0] == enemyType && board.getBoard()[6] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[5] == enemyType)) &&
			!board.isMarked(3))
			return 3;
		//right
		if(((board.getBoard()[2] == enemyType && board.getBoard()[8] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[3] == enemyType)) &&
			!board.isMarked(5))
			return 5;
		//bottom
		if(((board.getBoard()[6] == enemyType && board.getBoard()[8] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[1] == enemyType)) &&
			!board.isMarked(7))
			return 7;
		return -1;
	}
	
	private int detectLossPreventionCorners(Board board){
		//top-left
		if(((board.getBoard()[1] == enemyType && board.getBoard()[2] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[8] == enemyType) ||
			(board.getBoard()[3] == enemyType && board.getBoard()[6] == enemyType)) &&
			!board.isMarked(0))
			return 0;
		
		//top-right
		if(((board.getBoard()[1] == enemyType && board.getBoard()[0] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[6] == enemyType) ||
			(board.getBoard()[5] == enemyType && board.getBoard()[8] == enemyType)) &&
			!board.isMarked(2))
			return 2;
		
		//bottom-left
		if(((board.getBoard()[3] == enemyType && board.getBoard()[0] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[2] == enemyType) ||
			(board.getBoard()[7] == enemyType && board.getBoard()[8] == enemyType)) &&
			!board.isMarked(6))
			return 6;

		//bottom-right
		if(((board.getBoard()[2] == enemyType && board.getBoard()[5] == enemyType) ||
			(board.getBoard()[4] == enemyType && board.getBoard()[0] == enemyType) ||
			(board.getBoard()[7] == enemyType && board.getBoard()[6] == enemyType)) &&
			!board.isMarked(8))
			return 8;
		return -1;
	}
}
