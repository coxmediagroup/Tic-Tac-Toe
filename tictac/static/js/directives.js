'use strict';


angular.module('coxtactoe.directives', [])
  .directive('appVersion', ['version', function (version) {
    return function (scope, elm, attrs) {
      elm.text(version);
    };
  }]);
