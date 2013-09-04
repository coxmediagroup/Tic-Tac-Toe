'use strict';

angular.module('simple-games', 
  ['ngResource',
  'simple-games.controllers',
  'simple-games.filters',
  'simple-games.services',
  'simple-games.directives'],
  function ($interpolateProvider){
    $interpolateProvider.startSymbol('<[');
    $interpolateProvider.endSymbol(']>'),
  function($httpProvider) {
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  };
}).factory('simple-games', ['$http', function($http){

    var SimpleGames = function(data) {
        angular.extend(this, data);
    };

    SimpleGames.get = function(id) {
        return $http.get('/tictactoe/' + id).then(function(response) {
            return new Product(response.data);
        });
    };

    SimpleGames.prototype.update = function() {
        var product = this;
        return $http.put('/tictactoe/move/' + product.id + '/', product).then(function(response) {
            return response.data;
        });
    };

    return SimpleGames;
}]);
