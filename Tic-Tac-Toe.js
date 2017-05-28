<script type="text/javascript">

// Variables
var painted;//array to check if canvas !empty
var content;//array for what is on canvas
var winCombo;//for possible winning combinations
var turn = 0;
var canvasID;//for canvas id
var sqr;//hold actual canvas
var context;
var sqrsFilled = 0;
var w;
var y;

window.onload = function() {
  painted = new Array();
  content = new Array();
  winCombo = [[0, 1, 2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]];

  for(var i = 0; i < 9; i++) {//usually use length of array but since we know its size is 9 hardcoding is ok
    painted[i] = false;
    content[i] = '';
  }
}

function canvasClicked(sqrNum) {
  canvasID = "s" + sqrNum;
  sqr = document.getElementById(canvasID);
  context = sqr.getContext("2d"); //to draw on canvas

  if(painted[sqrNum - 1] == false) {//if square not used, use
    if(turn % 2 === 0) {
      //draw x TODO make this its own fucntion
      context.beginPath();
      context.moveTo(10, 10);
      context.lineTo(40, 40);
      context.moveTo(40, 10);
      context.lineTo(10, 40);
      context.stroke();
      context.closePath();
      content[sqrNum - 1] = 'X';//this canvas is marked with X
    }
    else {
      //draw circle TODO make this its own function
      context.beginPath();
			context.arc(25,25,20,0,Math.PI*2,true);
			context.stroke();
			context.closePath();
			content[sqrNum - 1] = 'O';//this canvas marked with O
    }
    turn++;//increment turn to know its next player
    painted[sqrNum - 1] = true;//this square is used
    sqrsFilled++; //increment number of sqrs filled

    checkWinners(content[sqrNum - 1]);

    if(sqrsFilled === 9) {
      alert("Game Over!");
      location.reload(true);
    }
  }
  else {
    alert("That space is occupied!");
  }
}
