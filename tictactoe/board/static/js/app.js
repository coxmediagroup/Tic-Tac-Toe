function TicTacToe() {
  this.moves = [];
  this.playing = false;
  this.play = function(pos) {
    if (this.playing === true) {
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
  };
  this.reset = function() {
    if (this.playing) {
      alert("AI is thinking.");
      return;
    }
    this.moves = [];
    this.draw();
  };
  // set up click handlers
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
  this.initialize();
}

var tictactoe = new TicTacToe();
