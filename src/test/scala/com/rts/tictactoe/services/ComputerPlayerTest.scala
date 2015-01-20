package com.rts.tictactoe.services

import org.scalatra.test.specs2._
import com.rts.tictactoe.models.GameBoard;

class ComputerPlayerTest extends MutableScalatraSpec {
  
  addServlet(classOf[ComputerPlayer], "/*")
  
  "GET /nextMove/ on ComputerPlayer" should {
    "return square index 4 when all squares are available" in {
      get("/nextMove/%20,%20,%20,%20,%20,%20,%20,%20,%20") {
        response.getContent() must_== "4";
        status must_== 200;
      }
    }
    "return square index 0 when only the middle square is taken" in {
      get("/nextMove/%20,%20,%20,%20,X,%20,%20,%20,%20") {
        response.getContent() must_== "0";
        status must_== 200;
      }
    }
    "return -1 when all squares are full" in {
      get("/nextMove/X,X,X,X,X,X,X,X,X") {
        response.getContent() must_== "-1";
        status must_== 200;
      }
    }
    "return winning square for computer" in {
      get("/nextMove/O,O,%20,%20,X,%20,X,%20,X") {
        response.getContent() must_== "2"
        status must_== 200;
      }      
    }
    "return winning square for player as defensive play" in {
      get("/nextMove/O,%20,%20,O,X,%20,X,O,X") {
        response.getContent() must_== "2";
        status must_== 200;
      }      
    }
  }
  
  "nextComputerMove " should {
    "return square index 4 when all squares are available" in {
      val gameBoard = new GameBoard(Array(" "," "," "," "," "," "," "," "," "));
      ComputerPlayer.nextComputerMove(gameBoard) must_== 4; 
    }
    "return square index 0 when only the middle square is taken" in {
      val gameBoard = new GameBoard(Array(" "," "," "," ","X"," "," "," "," "));
      ComputerPlayer.nextComputerMove(gameBoard) must_== 0; 
    }
    "return -1 when all squares are full" in {
      val gameBoard = new GameBoard(Array("X","X","X","X","X","X","X","X","X"));
      ComputerPlayer.nextComputerMove(gameBoard) must_== -1; 
    }
    "return winning square for computer" in {
      val gameBoard = new GameBoard(Array("O","O"," "," ","X"," ","X"," ","X"));
      ComputerPlayer.nextComputerMove(gameBoard) must_== 2; 
    }
    "return winning square for player as defensive play" in {
      val gameBoard = new GameBoard(Array("O"," "," ","O","X"," ","X","O","X"));
      ComputerPlayer.nextComputerMove(gameBoard) must_== 2; 
    }
    
  }
}