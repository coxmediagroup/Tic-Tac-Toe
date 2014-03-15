package com.blastedstudios.tictactoe.ui;

import java.util.ArrayList;
import java.util.Random;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.Touchable;
import com.badlogic.gdx.scenes.scene2d.ui.Button;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.Skin;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.ui.Window;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.blastedstudios.tictactoe.agent.ArtificialAgentSimple;
import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

public class MainWindow extends Window {
	private final Skin skin;
	private final Table boardTable;
	private final Random random = new Random();
	
	public MainWindow(final Skin skin){
		super("Tic Tac Toe", skin);
		this.skin = skin;
		boardTable = new Table(skin);
		generate(new Board(3));
		final Button newButton = new TextButton("New", skin);
		final Button exitButton = new TextButton("Exit", skin);
		newButton.addListener(new ClickListener() {
			@Override public void clicked(InputEvent event, float x, float y) {
				generate(new Board(3));
			}
		});
		exitButton.addListener(new ClickListener() {
			@Override public void clicked(InputEvent event, float x, float y) {
				Gdx.app.exit();
			}
		});
		add(boardTable);
		row();
		add(newButton);
		row();
		add(exitButton).colspan(2);
		pack();
		setX(Gdx.graphics.getWidth()/2 - getWidth()/2);
		setY(Gdx.graphics.getHeight()/2 - getHeight()/2);
	}
	
	private void generate(final Board board){
		boardTable.clear();
		boardTable.setTouchable(Touchable.enabled);
		final MarkTypeEnum playerType = random.nextInt(2) == 0 ? MarkTypeEnum.O : MarkTypeEnum.X,
				aiType = playerType == MarkTypeEnum.X ? MarkTypeEnum.O : MarkTypeEnum.X;
		final ArtificialAgentSimple ai = new ArtificialAgentSimple(aiType);
		final ArrayList<TextButton> boardButtons = new ArrayList<TextButton>(board.getBoard().length);
		for(int i=0; i<board.getBoard().length; i++){
			if(i>0 && i%board.getSpan() == 0)
				boardTable.row();
			final int location = i;
			final TextButton button = new TextButton(" ", skin);
			button.addListener(new ClickListener() {
				@Override public void clicked(InputEvent event, float x, float y) {
					try {
						board.mark(location, playerType);
						button.setText(playerType.printed());
						button.setTouchable(Touchable.disabled);
						if(board.getWinner() == MarkTypeEnum.NONE){
							int location = ai.turn(board);
							boardButtons.get(location).setText(aiType.printed());
							boardButtons.get(location).setTouchable(Touchable.disabled);
						}
						if(board.getWinner() != MarkTypeEnum.NONE &&
							board.getWinner() != MarkTypeEnum.DRAW){
							boardTable.setTouchable(Touchable.disabled);
							boardTable.row();
							boardTable.add(new Label(board.getWinner().printed() + " wins!", skin)).colspan(3);
							pack();
						}
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			});
			boardButtons.add(button);
			boardTable.add(button);
		}
	}
}
