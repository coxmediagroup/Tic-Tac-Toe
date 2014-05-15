'use strict';

/* Directives */

angular.module('simple-games.directives', []).
  directive('appVersion', function (version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  });