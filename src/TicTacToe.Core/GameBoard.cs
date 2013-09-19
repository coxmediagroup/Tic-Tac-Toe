namespace TicTacToe.Core
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    public class GameBoard
    {
        /// <summary>
        /// Positions and state of the board
        /// </summary>
        public IPlayer[][] BoardPositions { get; internal set; }

        internal static int[][] WinConditions;

        public GameBoard()
        {
            //Create three rows of three board positions
            this.BoardPositions = new IPlayer[3][];
            this.BoardPositions[0] = new IPlayer[3];
            this.BoardPositions[1] = new IPlayer[3];
            this.BoardPositions[2] = new IPlayer[3];

            WinConditions = new int[8][];
            WinConditions[0] = new[] { 0, 1, 2 };
            WinConditions[1] = new[] { 3, 4, 5 };
            WinConditions[2] = new[] { 6, 7, 8 };
            WinConditions[3] = new[] { 0, 3, 6 };
            WinConditions[4] = new[] { 1, 4, 7 };
            WinConditions[5] = new[] { 2, 5, 8 };
            WinConditions[6] = new[] { 0, 4, 8 };
            WinConditions[7] = new[] { 2, 4, 6 };
        }

        public bool IsPositionOccupied(int x, int y)
        {
            return this.BoardPositions[y][x] != null;
        }

        public void Occupy(IPlayer player, int x, int y)
        {
            if (this.IsPositionOccupied(x, y))
                throw new InvalidOperationException("Position " + x + ":" + y + " is already occupied.");
            this.BoardPositions[y][x] = player;
        }

        /// <summary>
        /// Unoccupy a position
        /// </summary>
        /// <param name="x">X Position</param>
        /// <param name="y">Y Position</param>
        public void UnOccupy(int x, int y)
        {
            this.BoardPositions[y][x] = null;
        }

        /// <summary>
        /// Determines if the game board positions are all taken
        /// </summary>
        /// <returns>True if the board is full, otherwise false</returns>
        public bool IsFull()
        {
            return BoardPositions.Any(x => x.Any(y => y == null)) == false;
        }

        /// <summary>
        /// Checks to see who the winner is for the current board state
        /// </summary>
        /// <returns><cref see="IPlayer"/> if there is a winner, or null if there is a tie or no winner yet.</returns>
        public IPlayer Winner()
        {
            foreach (var condition in WinConditions)
            {
                int x,y = 0;
                IndexToCoords(condition[0],out x, out y);
                var p1 = BoardPositions[y][x];
                IndexToCoords(condition[1],out x, out y);
                var p2 = BoardPositions[y][x];
                IndexToCoords(condition[2],out x, out y);
                var p3 = BoardPositions[y][x];

                if (p1 == null || p2 == null || p3 == null) continue;

                if (p1 == p2 && p2 == p3)
                {
                    return p1;
                }
            }

            return null;
        }

        internal void IndexToCoords(int idx, out int x, out int y)
        {
            x = idx % 3;
            y = idx / 3;
        }
    }
}