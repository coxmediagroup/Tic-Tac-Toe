package com.blastedstudios.tictactoe.agent;

import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

public class ArtificialAgentSimple extends Agent {
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
	@Override public void turn(Board board) {
		while(true)
			try{
				board.mark(choose(board), markType);
				return;
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
		if(board.getMiddle() == MarkTypeEnum.NONE)
			return 4;
		
		//middles are easier
		
		//top
		if(((board.getBoard()[0] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[0] != markType && board.getBoard()[2] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[7] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[7] != markType)) &&
			!board.isMarked(1))
			return 1;
		//left
		if(((board.getBoard()[0] == markType && board.getBoard()[6] == markType) ||
			(board.getBoard()[0] != markType && board.getBoard()[6] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[5] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[5] != markType)) &&
			!board.isMarked(3))
			return 3;
		//right
		if(((board.getBoard()[2] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[2] != markType && board.getBoard()[8] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[3] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[3] != markType)) &&
			!board.isMarked(5))
			return 5;
		//bottom
		if(((board.getBoard()[6] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[6] != markType && board.getBoard()[8] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[1] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[1] != markType)) &&
			!board.isMarked(7))
			return 7;
		
		//now for the corners
		
		//top-left
		if(((board.getBoard()[1] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[1] != markType && board.getBoard()[2] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[8] != markType) ||
			(board.getBoard()[3] == markType && board.getBoard()[6] == markType) ||
			(board.getBoard()[3] != markType && board.getBoard()[6] != markType) ||
			(board.getBoard()[6] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[6] != markType && board.getBoard()[2] != markType)) &&
			!board.isMarked(0))
			return 0;
		
		//top-right
		if(((board.getBoard()[1] == markType && board.getBoard()[0] == markType) ||
			(board.getBoard()[1] != markType && board.getBoard()[0] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[6] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[6] != markType) ||
			(board.getBoard()[5] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[5] != markType && board.getBoard()[8] != markType) ||
			(board.getBoard()[0] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[0] != markType && board.getBoard()[8] != markType)) &&
			!board.isMarked(2))
			return 2;
		
		//bottom-left
		if(((board.getBoard()[3] == markType && board.getBoard()[0] == markType) ||
			(board.getBoard()[3] != markType && board.getBoard()[0] != markType) ||
			(board.getBoard()[4] == markType && board.getBoard()[2] == markType) ||
			(board.getBoard()[4] != markType && board.getBoard()[2] != markType) ||
			(board.getBoard()[7] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[7] != markType && board.getBoard()[8] != markType) ||
			(board.getBoard()[0] == markType && board.getBoard()[8] == markType) ||
			(board.getBoard()[0] != markType && board.getBoard()[8] != markType)) &&
			!board.isMarked(6))
			return 6;
		
		//bottom-right
		//defaults if not much is down
		return 8;
	}
}
