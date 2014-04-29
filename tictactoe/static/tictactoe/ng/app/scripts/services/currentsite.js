'use strict';

angular.module('ticTacToeApp').factory('currentSite', function() {
  return {
    domain:window.current_site
  }
});
