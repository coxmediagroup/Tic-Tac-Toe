namespace TicTacToe.Core
{
    using System;
    using System.Linq;

    public class GameBoard
    {
        /// <summary>
        /// Positions and state of the board
        /// </summary>
        public IPlayer[][] BoardPositions { get; internal set; }

        public GameBoard()
        {
            //Create three rows of three board positions
            this.BoardPositions = Enumerable.Repeat(Enumerable.Repeat<IPlayer>(null, 3).ToArray(), 3).ToArray();
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
            return default(IPlayer);
        }
    }
}