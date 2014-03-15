package com.blastedstudios.tictactoe;

import com.blastedstudios.tictactoe.agent.Agent;
import com.blastedstudios.tictactoe.agent.ArtificialAgentSimple;
import com.blastedstudios.tictactoe.agent.TerminalAgent;
import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;
import com.blastedstudios.tictactoe.common.ModeEnum;

/**
 * The easiest iteration for tic-tac-toe is using the terminal (or console).
 * This will run in a terminal, prompting the user to enter data via the keyboard
 * to indicate which mode to put the program in and what space the user wishes to
 * mark.
 */
public class TerminalDriver {

	public static void main(String[] args) {
		while(true){
			switch(promptMode()){
			case PVP:{
				gameLoop(new Board(promptSpan()), 
						new TerminalAgent(MarkTypeEnum.X),
						new ArtificialAgentSimple(MarkTypeEnum.O));
				break;
			}case PVE:{
				gameLoop(new Board(3), 
						new TerminalAgent(MarkTypeEnum.X),
						new TerminalAgent(MarkTypeEnum.O));
				break;
			}case EVE:{
				gameLoop(new Board(3), 
						new ArtificialAgentSimple(MarkTypeEnum.X),
						new ArtificialAgentSimple(MarkTypeEnum.O));
				break;
			}case QUIT:
				System.exit(0);
			}
		}
	}
	
	/**
	 * This method prompts the user to enter the game mode. The game mode dictates
	 * whether the game will be pvp (player vs player), pve (player vs computer), 
	 * or eve (computer vs computer).
	 * 
	 * Upon naming this function getMode, I thought of states and if this should be 
	 * a state driven program. It is too simplistic, however, and while it would be
	 * mildly interesting to get an event driven console app, I'm just going to make
	 * a different gui later with many more capabilities.
	 */
	private static ModeEnum promptMode(){
		while(true){
			System.out.println("Please input " + ModeEnum.getDisplayNames());
			String input = System.console().readLine();
			if(	input.equalsIgnoreCase("exit") || input.equalsIgnoreCase("e") ||
				input.equalsIgnoreCase("quit") || input.equalsIgnoreCase("q"))
				return ModeEnum.QUIT;
			if(input.equalsIgnoreCase("pvp"))
				return ModeEnum.PVP;
			else if(input.equalsIgnoreCase("pve"))
				return ModeEnum.PVE;
		}
	}
	
	/**
	 * Prompt user for span (or width) of tic-tac-toe board. This is typically 3,
	 * but for pvp games may be any desired size
	 */
	private static int promptSpan(){
		while(true){
			System.out.println("Please input the desired board size, or 'quit' to close the application");
			String input = System.console().readLine();
			try{
				return Integer.parseInt(input);
			}catch(NumberFormatException e){
				System.out.println("Please input a valid number for board size");
			}
		}
	}
	
	/**
	 * I thought of a lot of dumb fancy programming stuff here for some reason. The plague
	 * of design patterns struck me, where I thought of adding an interface for agents
	 * which listen to mark events, then sends events (which the board would listen for),
	 * check the win state, and invoke another listener here if there is a win state. For this
	 * particular problem, I feel it over-engineers the issue, but perhaps in the python
	 * implementation I'll indulge myself in some lambda function handlers for this kind of thing.
	 * 
	 * What's the gang-of-four reference here - a monitor pattern I believe, or at least listener.
	 * There are always a few patterns that apply. So do I express this in code, have folks see
	 * I too verbosely and theoretically approach a simple problem? Do I stay agile/light and
	 * wait to implement functionality to avoid code bloat? I tend toward the latter now, but
	 * would express how I could go either way management directs me. Man was created to tend toward
	 * laziness/comfort, no? That's why I'm here Friday night at 11:12 after all, heh.
	 * 
	 * Feels kinda like answering a question that isn't there. Should I implement a design pattern
	 * where there's no one asking for a complex solution? Should I mock this unit test for
	 * an eventuality I know I'll never interact with? Could I make a plugin infrastructure using
	 * JSPF (like GDXworld on narfman0's github) to offer other listeners that could handle/render
	 * the information differently? Notification system... in tic-tac-toe?
	 * 
	 * These things I entertained, but the sooo heavy burden of programming struck me. Life is soooo hard
	 * (he said sarcastically). I suspect I'm more reverse engineering cox media group's intentions
	 * and what they'd want rather than engineering the project. A quandary they
	 * put me in, and here I lie rambling on Friday night whilst musing about this stuff.
	 * I suppose if I want to twist it to some other positive, that CMG as customer, I care to that degree
	 * to get the job done the way they want - props to me. 
	 */
	private static MarkTypeEnum gameLoop(Board board, Agent x, Agent o){
		while(true){
			MarkTypeEnum winner = takeTurn(board, x);
			if(winner == MarkTypeEnum.NONE)
				winner = takeTurn(board, o);
			if(winner != MarkTypeEnum.NONE){
				System.out.println(winner.name() + " is the winner!\n" + board);
				return winner;
			}
		}
	}
	
	private static MarkTypeEnum takeTurn(Board board, Agent agent){
		System.out.println("Player " + agent.getMarkType().name() + ", please input the position "
				+ "[0-" + board.getBoard().length + "]\n" + board);
		agent.turn(board);
		return board.getWinner();
	}
}
