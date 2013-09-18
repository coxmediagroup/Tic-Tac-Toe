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

        public void UnOccupy(int x, int y)
        {
            this.BoardPositions[y][x] = null;
        }
    }
}