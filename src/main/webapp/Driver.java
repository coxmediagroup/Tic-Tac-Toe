/**
 * 
 */

package webapp;
import java.util.Arrays;

/**
 * @author ryanmcdonald
 * 
 */
public class Driver {

     int[][] gameBoard    = new int[][] { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };
     int[][] boardX       = new int[][] { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };
     int[][] boardO       = new int[][] { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };

     /** display of board to depict **/
     int[][] boardDisplay = new int[][] { { 0, 0, 0 }, { 0, 0, 0 }, { 0, 0, 0 } };

     // Vertical Wins
     int[][] vwin1        = new int[][] { { 1, 1, 1 }, { 0, 0, 0 }, { 0, 0, 0 } };
     int[][] vwin2        = new int[][] { { 0, 0, 0 }, { 1, 1, 1 }, { 0, 0, 0 } };
     int[][] vwin3        = new int[][] { { 0, 0, 0 }, { 0, 0, 0 }, { 1, 1, 1 } };

     // horizontal wins
     int[][] hwin1        = new int[][] { { 1, 0, 0 }, { 1, 0, 0 }, { 1, 0, 0 } };
     int[][] hwin2        = new int[][] { { 0, 1, 0 }, { 0, 1, 0 }, { 0, 1, 0 } };
     int[][] hwin3        = new int[][] { { 1, 0, 0 }, { 0, 0, 1 }, { 0, 0, 1 } };

     // angular wins
     int[][] angwin1      = new int[][] { { 0, 0, 1 }, { 0, 1, 0 }, { 1, 0, 0 } };
     int[][] angwin2      = new int[][] { { 1, 0, 0 }, { 0, 1, 0 }, { 0, 0, 1 } };

     /**
      * 
      */
     public Driver() {
          System.out.println("\n\n---GAME BOARD MAPPING---\n\n");
          for (int i = 0; i < gameBoard.length; i++) {
               for (int j = 0; j < gameBoard.length; j++) {
                    System.out.print(gameBoard[i][j] + " ");
               }
               System.out.print("\n");
          }
     }

     /**
      * 
      */
     public void mergeBoards(int[][]... arrays) {

          System.out.println("--Display Board--");
          printMatrix(boardDisplay);

          for (int[][] arr : arrays) {

               for (int[] array : arr) {

                    for (int i = 0; i < array.length; i++) {
                         System.out.print(array[i]);

                         if (array[i] == 1) {
                              boardDisplay[i][i] = array[i];
                         }
                    }

                    System.out.print("\n");
                    // result[index++] = array;
               }
               System.out.print("\n");
          }

          System.out.println("--Display Board After--");
          printMatrix(boardDisplay);
     }

     /**
      * 
      * @param one
      * @param two
      */
     public boolean isWinner(int[][] one, int[][] two) {
          return Arrays.deepEquals(one, two);
     }

     /**
      * 
      * @param matrix
      */
     public void printMatrix(int[][] matrix) {

          System.out.println("Size: " + matrix.length);

          for (int i = 0; i < matrix.length; i++) {
               for (int j = 0; j < matrix.length; j++) {
                    System.out.print(matrix[i][j] + " ");
               }

               System.out.print("\n");
          }
     }

     /**
      * 
      */
     public void printWinningCombinations() {
          printMatrix(vwin1);
          System.out.println("\n\n------\n\n");
          printMatrix(vwin2);
          System.out.println("\n\n------\n\n");
          printMatrix(vwin3);
          System.out.println("\n\n------\n\n");

          printMatrix(hwin1);
          System.out.println("\n\n------\n\n");
          printMatrix(hwin2);
          System.out.println("\n\n------\n\n");
          printMatrix(hwin3);
          System.out.println("\n\n------\n\n");

          printMatrix(angwin1);
          System.out.println("\n\n------\n\n");
          printMatrix(angwin2);
          System.out.println("\n\n------\n\n");

     }

     /**
      * 
      * @param args
      */
     public static void main(String[] args) {
          Driver d = new Driver();
          System.out.println("\n\n------\n\n");
          d.printWinningCombinations();

          System.out.println("\n\n-----Compare-----\n\n");
          System.out.println(d.isWinner(d.angwin1, d.angwin1));

          System.out.println("\n\n-----MERGE-----\n\n");
          d.mergeBoards(d.angwin1, d.angwin2);

     }
}
