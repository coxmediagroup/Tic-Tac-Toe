(function(angular) {
  'use strict';

  var app = angular.module('coxtactoe.websocket', []);

  app.factory('socketio',
  ['$rootScope', '$document', 'io', function($rootScope, $document, io) {

    if (!socket) {
      console.log($document[0].domain);
      var url = 'http://' + $document[0].domain + ':8001',
          socket = io.connect(url);
    }

    var scopeApplyCallback = function(callback) {
      if (typeof callback === 'function') {
        return function() {
          var args = arguments;
          // Call callback, updating app $rootScope so
          // angular is aware of $rootScope var changes.
          $rootScope.$apply(function() {
            callback.apply(socket, args);
          });
        };
      }
    };

    var on = function(socket_event, callback) {
      socket.addListener(socket_event, scopeApplyCallback(callback));
    };

    var emit = function(socket_event, data, callback) {
      if (typeof callback === 'function') {
        socket.emit(socket_event, data, scopeApplyCallback(callback));
      } else {
        socket.emit(socket_event, data);
      }
    };

    var removeAllListeners = function (socket_event, callback) {
      socket.removeAllListeners(socket_event, function() {
        var args = arguments;
        $rootScope.$apply(function () {
          callback.apply(socket, args);
        });
      });
    };

    return {
      on: on,
      emit: emit,
      removeAllListeners: removeAllListeners
    };
  }]);

})(window.angular);
