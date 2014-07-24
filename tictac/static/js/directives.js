(function(angular) {
  'use strict';

  angular.module('coxtactoe.directives', [])
    .directive('aiMsgArea', function() {
      return {
        restrict: 'E',
        templateUrl: '/static/templates/coxtactoe/partials/ai-msg-area.html',
        replace: 'true'
      };
    })
    .directive('ticTacToe', function() {
      return {
        restrict: 'E',
        templateUrl: '/static/templates/coxtactoe/partials/tictactoe.html',
        replace: 'true'
      };
    })
    .directive('gameLog', function(){
      return {
        restrict: 'E',
        templateUrl: '/static/templates/coxtactoe/partials/game-log.html',
        replace: 'true'
      };
    })
    .directive('gameOverMsg', function(){
      return {
        restrict: 'E',
        templateUrl: '/static/templates/coxtactoe/partials/game-over-msg.html',
        replace: 'true'
      };
    });

})(window.angular);
