namespace TicTacToe.Core.Utils
{
    using System;
    using System.Security.Cryptography;

    /// <summary>
    /// Uses a RNGCryptoServiceProvider to provide better randoms.
    /// Borrowed from an open source project I run https://github.com/kellyelton/OCTGN/blob/master/octgnFX/Octgn.Library/Paths.cs
    /// </summary>
    public class RngRandom 
    {
        #region Singleton
        internal static RngRandom Context { get; set; }
        private static readonly object RngRandomSingletonLocker = new object();
        public static RngRandom Instance
        {
            get
            {
                if (Context != null)
                {
                    return Context;
                }
                lock (RngRandomSingletonLocker)
                {
                    return Context ?? (Context = new RngRandom());
                }
            }
        }

        #endregion Singleton

        private readonly RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider();

        /// <summary>
        /// Gets next random integer between 0 and Int32.MaxValue
        /// </summary>
        /// <returns>Next random integer between 0 and Int32.MaxValue</returns>
        public Int32 Next()
        {
            var uint32Buffer = new byte[4];
            this.rng.GetBytes(uint32Buffer);
            return BitConverter.ToInt32(uint32Buffer, 0) & 0x7FFFFFFF;
        }
        /// <summary>
        /// Gets a random integer between 0 and maxValue
        /// </summary>
        /// <param name="maxValue">Max value</param>
        /// <returns>Random integer between 0 and maxValue</returns>
        public Int32 Next(Int32 maxValue)
        {
            if (maxValue < 0) throw new ArgumentOutOfRangeException("maxValue");
            return this.Next(0, maxValue);
        }

        /// <summary>
        /// Gets a random number between minValue and maxValue
        /// </summary>
        /// <param name="minValue">Minimum Value</param>
        /// <param name="maxValue">Maximum Value</param>
        /// <returns>A Random integer between minValue and maxValue</returns>
        public Int32 Next(Int32 minValue, Int32 maxValue)
        {
            if (minValue > maxValue) throw new ArgumentOutOfRangeException("minValue");
            if (minValue == maxValue) return minValue;
            Int64 diff = maxValue - minValue;
            var uint32Buffer = new byte[4];
            while (true)
            {
                this.rng.GetBytes(uint32Buffer);
                var rand = BitConverter.ToUInt32(uint32Buffer, 0);
                const long Max = (1 + (Int64)UInt32.MaxValue);
                var remainder = Max % diff;
                if (rand < Max - remainder)
                {
                    return (Int32)(minValue + (rand % diff));
                }
            }
        }
    }
}
