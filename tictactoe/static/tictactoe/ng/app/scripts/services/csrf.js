'use strict';

angular.module('ticTacToeApp') .service('csrf', 
['$http',
function Gameboard($http) {
  var cookieValue = '';
  if (document.cookie) {
    var dc = document.cookie;
    // why yes, I do know regular expressions
    var r = dc.match(/(^|;)\s*csrftoken\s*=\s*(.*?)(;|$)/);
    if (r) {
      cookieValue = decodeURIComponent(r[2]);
    }
  }
  $http.defaults.headers.common['X-CSRFToken'] = cookieValue;
  return cookieValue;
}]);