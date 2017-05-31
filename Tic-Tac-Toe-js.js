// Variables
var painted;//array to check if canvas !empty
var content;//array for what is on canvas
var winCombo;//for possible winning combinations
var turn = 0;
var canvasID;//for canvas id
var sqr;//hold actual canvas
var context;//for drawing on canvas
var sqrsFilled;
var y;//for user answer to playAgain?
var userXO;

window.onload = function() {//initailize vars 
  sqrsFilled = 0;
  painted = new Array();
  content = new Array();
  winCombo = [[0, 1, 2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]];

  for(var i = 0; i < 9; i++) {//usually use length of array but since we know its size is 9 hardcoding is ok
    painted[i] = false;
    content[i] = '';
  }
}

function drawX(sqrNum) //draws X in sqaure
  context.beginPath();
  context.moveTo(10, 10);
  context.lineTo(40, 40);
  context.moveTo(40, 10);
  context.lineTo(10, 40);
  context.closePath();
  context.strokeStyle='#ffffff';
  context.stroke();
  content[sqrNum - 1] = 'X';//this canvas is marked with X
}

function drawO(sqrNum) {//draws O in sqaure
  context.beginPath();
  context.arc(25, 25, 20, 0, Math.PI*2, true);
  context.closePath();
  context.strokeStyle='#ffffff';
  context.stroke();
  content[sqrNum - 1] = 'O';//this canvas marked with O
}

function canvasClicked(sqrNum) {
  if(userXO === undefined) {//if user did not select a symbol it autoselects X
    var choiceDiv = document.getElementById("XorO");
    alert("X or O not selected. You are X");
    userXO = "x";
    choiceDiv.style.display = 'none';
  }
  canvasID = "s" + sqrNum;
  sqr = document.getElementById(canvasID);
  context = sqr.getContext("2d"); //to draw on canvas with specific ID

  if(painted[sqrNum - 1] === false) {//if square not used, use
    if(turn % 2 === 0) {//whichever symbol user picked goes first
      if(userXO === "x") {
        drawX(sqrNum);
      }
      else {
        drawO(sqrNum);
      }
    }
    else {//comp symbol goes second
      if(userXO === "x") {
        drawO(sqrNum);
      }
      else {
        drawX(sqrNum);
      }
    }
    turn++;//increment turn to know its next player
    painted[sqrNum - 1] = true;//this square is used
    sqrsFilled++; //increment number of sqrs filled

    checkWinners(content[sqrNum - 1]);//check for winner after each move

    if(sqrsFilled === 9) {//check if board is full. if so, ask to play again
      alert("Game Over!");
      playAgain();
    }
  }
  else {
    alert("That space is occupied!");
  }
}

function checkWinners(symbol) {//checks if anyone won the game
  for(var i = 0; i < winCombo.length; i++) {//go through and check if either X or O has winning combo
    if(content[winCombo[i][0]] == symbol && content[winCombo[i][1]] == symbol && content[winCombo[i][2]] == symbol) {
      if(symbol === userXO.toUpperCase()) {
        alert("You Won!");
      }
      else {
        alert("Computer Won!");
      }
      playAgain();
    }
  }
}

function playAgain() {// ask to play again
  y = confirm("Play again?");

  if(y === true) {
    alert("Lets play again!");
    location.reload(true);
  }
  else {
    alert("See you, space cowboy.");
  }
}

function userChoice(choice) {//checks which symbol user wants to use
  var choiceDiv = document.getElementById("XorO");
  if(choice === "x") {
    userXO = "x";
  }
  else if(choice === "o") {
    userXO = "o";
  }
  choiceDiv.style.display = 'none';
}
