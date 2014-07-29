(function(angular) {
  'use strict';

  var app = angular.module('coxtactoe', [
    'coxtactoe.websocket',
    'coxtactoe.directives',
    'coxtactoe.controllers'
  ]);
  app.constant('$', window.$);
  app.constant('io', window.io);

})(window.angular);
