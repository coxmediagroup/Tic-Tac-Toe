/*
 * ttt.c
 *
 * Implements the game of tic-tac-toe.
 *
 * Approach:
 * 	- Represent the board as a bitfield
 * 	- Check for moves with bitwise arithmetic
 * 	- Main function is "stateless"; given a board state it computes the next
 * 	player to move and returns their best move.
 * 	- UI logic is decoupled from game logic; possibly even a separate process.
 * 	Execution might look like:
 * 		cat board.txt | ./tttread | ./ttt | ./tttshow
 * 	- Benchmarks, graphs of games, memory use vs. time :)
 *
 * Board is represented as a 32-bit integer:
 * 	- Bits 0-9: 1 if X occupies a position
 * 	- Bits 10-18: 1 if O occupies a position
 * 	- Bits 19-31: Unused. Maybe report game state.
 * */

#include <stdint.h>
#include <stdio.h>

/* "C does not provide a standard boolean type, because picking one involves a
 * space/time tradeoff which is best decided by the programmer.  (Using an int
 * for a boolean may be faster, while using char may save data space.)"
 * http://www.lysator.liu.se/c/c-faq/c-8.html
 */
typedef unsigned int bool;
enum bool {false, true};

uint32_t states[0x40000];
uint32_t wins[2][8] = { {
	0b000000000111000000,
	0b000000000000111000,
	0b000000000000000111,
	0b000000000100100100,
	0b000000000010010010,
	0b000000000001001001,
	0b000000000100010001,
	0b000000000001010100,
}, {
	0b111000000000000000,
	0b000111000000000000,
	0b000000111000000000,
	0b100100100000000000,
	0b010010010000000000,
	0b001001001000000000,
	0b100010001000000000,
	0b001010100000000000,
} };

uint32_t m2(uint32_t b) {
    /* vertical mirror board */
    uint32_t x;
    x = ((b >> 6) ^ b) & 0b000000111000000111;
    b ^= ((x << 6) | x);
    return b;
}

uint32_t r1(uint32_t b) {
    /* rotate board */
    uint32_t x;
    x = ((b >> 2) ^ b) & 0b001100011001100011;
    b ^= ((x << 2) | x);
    x = ((b >> 3) ^ b) & 0b000100001000100001;
    b ^= ((x << 3) | x);
    x = ((b >> 5) ^ b) & 0b000001001000001001;
    b ^= ((x << 5) | x);
    return b;
}

uint32_t valid_state(uint32_t q) {
	/* Sanity check the board state. A valid board:
	 *
	 * - Has no X occupying the same position as O
	 * - Has count(X moves) - count(O moves) = 0 or 1.
	 * - Has exactly 1 or 0 winners
	 */
}

bool x_just_moved(uint32_t q) {
	/* Determine if the player most recently to moved given a valid board state
	 * was "X". Returns:
	 * 		0 (false): O just moved; X moves next
	 * 		1 (true): X just moved; O moves next
	 */
	uint32_t r = 0; /* return value */

	/* Strategy: if the total number of moves (1s) is even, X moves next. */

	/* Combine the X and O board, mask anything else. */
	q = (q | (q >> 9)) & 0b111111111;

	/* This and various other ways to count the number of bits set:
	 * http://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetKernighan
	 */
	for (r = 0; q; r++) {
		q &= q - 1; // clear the least significant bit set
	}
	return r;
}

bool winning_move(uint32_t input) {
	/* Given a valid board state, determine if the most recent player to move
	 * has won. Returns:
	 * 		0 (false): No win
	 * 		1 (true): player has won
	 */
	int i; /* loop index */
	int j; /* player index */

	/* We need test only the win patterns for the player who has most recently
	 * moved. */
	if (x_just_moved(input)) {
		j = 0;
	} else {
		j = 1;
	}

	for (i=0; i<8; i++) {
		if (input & wins[j][i] == wins[j][i]) {
			return true;
		}
	}
	return false;
}

uint32_t _next_state(uint32_t input) {
	/* Recursive helper to next_state.
	 *
	 * 
	 *
	 * Strategy: Perform a breadth-first recursive search for a winning state.
	 */
	int i;
	int score, best_score = 0;
	uint32_t state, best_state;

	for (i = 0; i<8; i++) {
		/* If the space is occupied, skip. */
		if (0xb1000000001<<i & input) {
			continue;
		}

		state = input & player<<i;
		score = minimax(state, 9)
		if score > best_score {
			best_score = score;
			best_state = state;
		}

		/* We won't do any better than an immediate win... */
		if (best_score == 9) {
			break;
		}
	}
	return best_state;
}

uint32_t next_state(uint32_t input) {
	/* Given a valid board state, compute and return the board state showing
	 * the best next move. This is just a memoization function for
	 * _next_state(). */
	if (!states[input]) {
		states[input] = _next_state(input)
	}
	return states[input];
}


int minimax(uint32_t node, char depth) {
	if winning_move(input & player<<i) {
		return depth;
	}
	for (i = 0; i<8; i++) {
		/* If the space is occupied, skip. */
		if (0xb1000000001<<i & input) { continue; }
		if winning_move(input & player<<i) {
			return input & player<<i;
		}
	}
}

void init() {
	int i;
	/* initialize DP work area */
	for (i=0; i<0x40000; i++) {
		states[i] = 0;
	}
}

void print_state(uint32_t state) {
	char output[13];
	output[3] = output[7] = output[11] = '\n';
	output[12] = '\0';
	int i; /* index */
	for (i=0; i<9; i++) {
		if (state & 1) {
			output[i + i/3] = 'X';
		} else {
			output[i + i/3] = '-';
		}
		state = state>>1;
	}
	for (i=0; i<9; i++) {
		if (state & 1) {
			output[i + i/3] = 'O';
		}
		state = state>>1;
	}
	printf("%s\n", output);
}

int main(int argc, char **argv) {
	int i, j;
	init();
	for (j=0; j<2; j++) {
		for (i=0; i<8; i++) {
			print_state(wins[j][i]);
		}
	}
	return 0;
}

