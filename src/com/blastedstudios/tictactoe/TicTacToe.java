package com.blastedstudios.tictactoe;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.backends.lwjgl.LwjglApplication;
import com.blastedstudios.tictactoe.ui.MainScreen;

public class TicTacToe extends Game{
	@Override public void create () {
		setScreen(new MainScreen());
	}
	
	public static void main (String[] argv) {
		new LwjglApplication(new TicTacToe(), "TicTacToe", 300, 400, true);
	}
}
