define([
  // Libraries
  'jquery',
  'underscore',
], function(
  $,
  _
) {
  'use strict';

  var winningStates = [
    [0,1,2], [3,4,5], [6,7,8], //rows
    [0,3,6], [1,4,7], [2,5,8], //columns
    [0,4,8], [2,4,6], // diagonals
  ];

  function TicTacToe() {
    this.moves = [];
    this.gameOver = false;
    this.playing = false;
    this.play = function(pos) {
      if (this.gameOver || this.moves.length === 9) {
        alert("The game is over.");
        return;
      }
      if (this.playing) {
        return;
      }
      if (_.contains(this.moves, pos)) {
        return;
      }
      this.playing = true;
      this.moves.push(pos);
      this.draw();
      this.playing = false;
      this.getRecommendedPlay();
    };
    this.getRecommendedPlay = function() {
      var url = "/api/recommended_play/";
      this.playing = true;
      $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
          moves: this.moves
        }),
        contentType: "application/json",
        success: function(data) {
          this.playing = false;
          this.moves = data.moves;
          this.draw();
        }.bind(this),
        error: function(xhr, status, err) {
          console.error(url, status, err.toString());
          this.playing = false;
        }.bind(this)
      });
    };
    this.draw = function() {
      $("#board .cell").each(function(elem) {
        $(this).text("");
      });

      _.each(this.moves, function(move, idx) {
        var token = idx % 2 ? "O" : "X";
        var elem = $("#pos" + move);
        elem.text(token);
      });

      this.checkWin();
      this.checkTie();
    };
    this.reset = function() {
      if (this.playing) {
        alert("AI is thinking.");
        return;
      }
      this.moves = [];
      this.draw();
      $("#board .cell").removeClass("win").removeClass("tie");
      this.gameOver = false;
    };
    this.checkWin = function() {
      var p1 = {}, p2 = {};
      var winningState = null;
      var hasWin = false;
      var i,x,y,z = null;
      var move = null;

      for (i = 0; i < this.moves.length; i++) {
        move = this.moves[i];
        if (i % 2 === 1) {
          p1[move] = true;
        } else {
          p2[move] = true;
        }
      }

      for (i = 0; i < winningStates.length; i++) {
        winningState = winningStates[i];
        x = winningState[0];
        y = winningState[1];
        z = winningState[2];
        if ((p1[x] && p1[y] && p1[z]) || (p2[x] && p2[y] && p2[z])) {
          hasWin = true;
          break;
        }
      }

      if(hasWin) {
        _.each(winningState, function(num) {
          $("#pos" + num).addClass("win");
        });
        this.gameOver = true;
      }
    };
    this.checkTie = function() {
      if (this.moves.length === 9) {
        $("#board .cell").addClass("tie");
      }
    };
    this.initialize = function () {
      var that = this;

      $("#board .cell").each(function(idx, obj) {
        $(obj).click(function() {
          that.play(idx);
        });
      });

      $("#reset").click(function() {
        that.reset();
      });
    };
  }

  return TicTacToe;

});
