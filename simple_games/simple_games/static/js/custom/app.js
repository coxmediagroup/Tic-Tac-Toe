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
});
