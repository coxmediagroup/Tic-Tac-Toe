(function(angular) {
  'use strict';

  var app = angular.module('coxtactoe.controllers', ['coxtactoe.websocket']);

  app.controller('AiMsgAreaCtrl',
  ['$scope', 'socketio', function($scope, socketio) {

    var socket = socketio;

    //  Scope Variables  //////////////////////////////////////////////////////
    $scope.ai_msg_queue = [];
    $scope.ai_msg_rendering = false;

    //  Helper Functions  /////////////////////////////////////////////////////
    var log_ai_msg = function(msg) {
      var log_msg = [
        '<br>[recv] ai_msg: MarvMin, the melancholy minmax AI, said:<br>',
        Array(8).join('&nbsp;'), '<em class="ai-said">', msg, '</em>'];
      angular.element('#log').append(log_msg.join(''));
    };

    var teletype_keypress = function(msg, char, el) {
      var box = el,
          key_delay = 10 * char;
      setTimeout(function() {
        box.text(box.text() + msg[char]);
      }, key_delay);
    };

    var render_ai_msg = function(ai_msg) {
      var msg = ai_msg,
          box = $('#dialog'),
          delay_per_char = 65,
          hide_delay = msg.length * delay_per_char;
      return (function() {
        $scope.ai_msg_rendering = true;
        box
          .fadeTo('fast', 0.8, function() {
            for (var i = 0, len = msg.length; i < len; i++) {
              teletype_keypress(msg, i, box);
            }
          })
          .delay(hide_delay)
          .text('')
          .fadeTo('fast', 0.0, function() {
            $scope.ai_msg_rendering = false;
          });
      });
    };

    //  AI Message Event Handlers  ////////////////////////////////////////////
    socket.on('ai_msg', function(data) {
      log_ai_msg(data.msg);
      $scope.ai_msg_queue.push(render_ai_msg(data.msg));
    });

    socket.on('error', function(data) {
      angular.element('#log')
        .append('<br>[recv] error: msg: <em>' + data.msg + '</em>')
        .append('<br>[recv] error: traceback: <em>' + data.traceback + '</em>');
      $scope.ai_msg_queue.push(render_ai_msg(data.msg));
    });

    //  AI Msg Queue Runner  //////////////////////////////////////////////////
    (function() {
      // Consumes AI msg queue, rendering msg dialog boxes in serial
      setInterval(function() {
        if ($scope.ai_msg_queue.length === 0) { return; }
        if ($scope.ai_msg_rendering) { return; }
        var render_ai_msg = $scope.ai_msg_queue.shift();
        render_ai_msg();
      }, 500);
    })();

  }]);


  app.controller('CoxtactoeCtrl',
  ['$scope', '$window', 'socketio', function($scope, $window, socketio) {

    var socket = socketio,
        path = $window.location.pathname.split('/'),
        game_id = path[path.length - 1];

    //  Scope Variables  //////////////////////////////////////////////////////
    $scope.squares = [];
    $scope.sq_classes = [];
    $scope.game_id = game_id;

    //  Scope Methods  ////////////////////////////////////////////////////////
    $scope.hoverClass = function(square, mouseover) {
      // No hover bg img when square already taken
      if (square === 'X' || square === 'O') { return 'taken'; }
      // Set square hover bg img to match human player's xo_choice
      if (mouseover) { return $scope.xo_choice + '-hover'; }
      return '';
    };

    $scope.move = function(square_idx) {
      var move = { square: square_idx };
      if (!$scope.game_over) {
        socket.emit('move', move);
        angular.element('#log').append([
          '<br>[send] move: <em>', JSON.stringify(move), '</em>'].join(''));
      }
    };

    //  Game State Event Handlers  ////////////////////////////////////////////
    socket.on('connect', function() {
      socket.emit('connect');
      angular.element('#log')
        .append('<br>[send] msg: <em>Connected</em>')
        .append('<br>[send] join: <em>Join game ' + game_id + '</em>');
      socket.emit('join', {game_id: game_id});
    });

    socket.on('msg', function(data) {
      angular.element('#log')
        .append('<br>[recv] msg: <em>' + data.msg + '</em>');
    });

    // Updates local game state w/ game data sent from server over WebSocket.
    socket.on('state', function(state_json) {
      angular.element('#log')
        .append('<br>[recv] state: <em>' + state_json + '</em>');
      var state = JSON.parse(state_json);

      if (state.board) {
        $scope.squares = state.board;
      }

      if (state.xo_choice) {
        $scope.xo_choice = state.xo_choice;
      }

      if (state.lost === true) {
        $scope.game_over = true;
        $scope.game_over_msg = 'YOU LOSE';
        $('.game-over-text').animate({opacity: 1}, 250);
      }

      if (state.tied === true) {
        $scope.game_over = true;
        $scope.game_over_msg = 'TIE GAME';
        $('.game-over-text').animate({opacity: 1}, 250);
      }
    });

  }]);

})(window.angular);

