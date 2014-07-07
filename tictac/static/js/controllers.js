app.controller('CoxtactoeCtrl', ['$scope', function($scope) {
  'use strict';

  var socket = io.connect('http://' + document.domain + ':8001');
  var path = window.location.pathname.split('/');
  var game_id = path[path.length - 1];
  var squares = [
    {id: 0, marker: ''},
    {id: 1, marker: ''},
    {id: 2, marker: ''},
    {id: 3, marker: ''},
    {id: 4, marker: ''},
    {id: 5, marker: ''},
    {id: 6, marker: ''},
    {id: 7, marker: ''},
    {id: 8, marker: ''}
  ];

  // Scope Variables
  $scope.game_over_msg = '';
  $scope.squares = squares;
  $scope.game_id = game_id;
  $scope.dialog_queue = [];
  $scope.dialog_rendering = false;


  //  Scope Methods  ///////////////////////////////////////////////////////////
  $scope.squareTaken = function(square) {
    return square.marker === '' ? '' : 'taken';
  };
  $scope.move = function(square) {
    var move = { square: square.id };
    if (!$scope.game_over) {
      socket.emit('move', move);
      $('#log').append([
        '<br>[send] move: <em>', JSON.stringify(move), '</em>'].join(''));
    }
  };


  //  Helper Functions  ////////////////////////////////////////////////////////
  var update_player_xo_choice = function(xo_choice) {
    // Push xo_choice to $scope for use in move() calls from game form
    $scope.$apply(function() {
      $scope.xo_choice = xo_choice;
    });
    // Set square hover bg img to match human player's xo_choice
    $('#tictactoe div').hover(
        function() {
          $(this).not('.taken').addClass(xo_choice + '-hover');
        },
        function() {
          $(this).not('.taken').removeClass('X-hover O-hover');
        });
  };

  var update_local_game_state = function(board) {
    $scope.$apply(function() {
      for (var i = 0; i < board.length; i++) {
        if (board[i] === 'X' || board[i] === 'O') {
          $scope.squares[i].marker = board[i];
        }
        $('#tictactoe div').removeClass('X-hover O-hover');
      }
    });
  };

  var log_ai_msg = function(msg) {
    var log_msg = [
      '<br>[recv] ai_msg: MarvMin, the melancholy minmax AI, said:<br>',
      Array(8).join('&nbsp;'), '<em style="color: #fc6">', msg, '</em>'];
    $('#log').append(log_msg.join(''));
  };

  var teletype_keypress = function(msg, char, el) {
    var key_delay = 10 * char,
        box = el;
    setTimeout(function() {
      box.text(box.text() + msg[char]);
    }, key_delay);
  };

  var render_ai_msg = function(ai_msg) {
    var msg = ai_msg,
        box = $('#dialog'),
        delay_per_char = 70,
        hide_delay = msg.length * delay_per_char;
    return (function() {
      $scope.dialog_locked = true;
      box
          .fadeTo('fast', 0.8, function() {
            for (var i = 0; i < msg.length; i++) {
              teletype_keypress(msg, i, box);
            }
          })
          .delay(hide_delay)
          .text('')
          .fadeTo('fast', 0.0, function() {
            $scope.dialog_locked = false;
          });
    });
  };


  //  Socket.io Event Handlers  ////////////////////////////////////////////////
  socket.on('connect', function() {
    socket.emit('connect');
    $('#log')
        .append('<br>[send] msg: <em>Connected</em>')
        .append('<br>[send] join: <em>Join game ' + game_id + '</em>');
    socket.emit('join', {game_id: game_id});
  });

  socket.on('msg', function(data) {
    $('#log').append('<br>[recv] msg: <em>' + data.msg + '</em>');
  });

  socket.on('ai_msg', function(data) {
    log_ai_msg(data.msg);
    $scope.$apply(function() {
      $scope.dialog_queue.push(render_ai_msg(data.msg));
    });
  });

  socket.on('error', function(data) {
    $('#log')
        .append('<br>[recv] error: msg: <em>' + data.msg + '</em>')
        .append('<br>[recv] error: traceback: <em>' + data.traceback + '</em>');
    $scope.$apply(function() {
      $scope.dialog_queue.push(render_ai_msg(data.msg));
    });
  });

  socket.on('state', function(state_json) {
    $('#log').append('<br>[recv] state: <em>' + state_json + '</em>');
    var state = JSON.parse(state_json);

    if (state.xo_choice === 'X' || state.xo_choice === 'O') {
      update_player_xo_choice(state.xo_choice);
    }

    if (state.board !== undefined) {
      update_local_game_state(state.board);
    }

    if (state.lost === true) {
      $scope.$apply(function() {
        $scope.game_over = true;
        $scope.game_over_msg = 'YOU LOSE';
      });
      $('.game-over-text').animate({opacity: 1}, 250);
    }

    if (state.tied === true) {
      $scope.$apply(function() {
        $scope.game_over = true;
        $scope.game_over_msg = 'TIE GAME';
      });
      $('.game-over-text').animate({opacity: 1}, 250);
    }
  });


  //  AI msg box queue runner  /////////////////////////////////////////////////
  // Watches AI msg queue and renders msg dialog boxes in serial
  (function() {
    setInterval(function() {
      if ($scope.dialog_queue.length === 0) { return; }
      if ($scope.dialog_rendering) { return; }
      var render_dialog = $scope.dialog_queue.shift();
      render_dialog();
    }, 500);
  })();

}]);


