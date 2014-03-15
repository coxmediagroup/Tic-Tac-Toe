package com.blastedstudios.tictactoe.agent;

import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

/**
 * Agent class for A.I. or player. An agent has a mark type and can be set to
 * autonomy
 */
public abstract class Agent {
	protected final MarkTypeEnum enemyType, markType;
	
	public Agent(MarkTypeEnum markType){
		this.markType = markType;
		this.enemyType = markType == MarkTypeEnum.O ? MarkTypeEnum.X : MarkTypeEnum.O;
	}

	public MarkTypeEnum getMarkType() {
		return markType;
	}

	public MarkTypeEnum getEnemyType() {
		return enemyType;
	}
	
	public abstract void turn(Board board);
}
