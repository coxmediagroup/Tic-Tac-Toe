package com.blastedstudios.tictactoe.board;

public enum MarkTypeEnum {
	NONE, X, O;

	public String printed(){
		if(this == NONE)
			return " ";
		return name();
	}
}