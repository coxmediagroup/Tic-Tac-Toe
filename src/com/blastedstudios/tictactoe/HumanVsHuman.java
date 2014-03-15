package com.blastedstudios.tictactoe;

import com.blastedstudios.tictactoe.agent.Agent;
import com.blastedstudios.tictactoe.agent.TerminalAgent;
import com.blastedstudios.tictactoe.board.Board;
import com.blastedstudios.tictactoe.board.MarkTypeEnum;

public class HumanVsHuman {

	public static void main(String[] args) {
		boolean play = true;
		while(play){
			System.out.println("Please input the desired board size, or 'quit' to close the application");
			String input = System.console().readLine();
			if(input.equalsIgnoreCase("exit") || input.equalsIgnoreCase("e") ||
				input.equalsIgnoreCase("quit") || input.equalsIgnoreCase("q"))
				play = false;
			else{
				try{
					int span = Integer.parseInt(input);
					MarkTypeEnum winner = gameLoop(new Board(span), 
							new TerminalAgent(MarkTypeEnum.X),
							new TerminalAgent(MarkTypeEnum.O));
					System.out.println(winner.name() + " is the winner!");
				}catch(NumberFormatException e){
					System.out.println("Please input a valid number for board size");
				}
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
			x.turn(board);
			MarkTypeEnum winner = board.getWinner();
			if(winner == MarkTypeEnum.NONE){
				o.turn(board);
				winner = board.getWinner();
			}
			if(winner != MarkTypeEnum.NONE)
				return winner;
		}
		
	}
}
