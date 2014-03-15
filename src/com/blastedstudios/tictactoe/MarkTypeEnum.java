package com.blastedstudios.tictactoe;

public enum MarkTypeEnum {
	NONE, X, O;

	public String printed(){
		if(this == NONE)
			return " ";
		return name();
	}
}