package com.blastedstudios.tictactoe.common;

public enum ModeEnum {
	QUIT("Quit <q>"), 
	EVE("Computer vs Computer <eve>"), 
	PVE("Player vs Computer <pve>"), 
	PVP("Player vs Player <pvp>");
	
	private final String displayName;
	
	private ModeEnum(String displayName){
		this.displayName = displayName;
	}

	public String getDisplayName() {
		return displayName;
	}
	
	public static String getDisplayNames(){
		StringBuffer buffer = new StringBuffer();
		for(int i=0; i < values().length; i++){
			buffer.append(values()[i].displayName);
			if(i < values().length-1)
				buffer.append(", ");
		}
		return buffer.toString();
	}
}
