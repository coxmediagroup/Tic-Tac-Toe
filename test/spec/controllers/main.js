'use strict';

describe('Controller: MainCtrl', function () {

  // load the controller's module
  beforeEach(module('TicTacToeApp'));

  var MainCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MainCtrl = $controller('MainCtrl', {
      $scope: scope
    });
  }));

  it('newRow should be able to identify the begining of a new row of cells', function () {
    expect(scope.newRow(0)).toBe(true);
    expect(scope.newRow(3)).toBe(true);
    expect(scope.newRow(6)).toBe(true);
  });
  
  it('newRow should identify cells not being the begining of a new row', function () {
    expect(scope.newRow(1)).toBe(false);
    expect(scope.newRow(2)).toBe(false);
    expect(scope.newRow(5)).toBe(false);
  });
  
  it('endRow should be able to identify the end of a row of cells', function () {
    expect(scope.endRow(2)).toBe(true);
    expect(scope.endRow(5)).toBe(true);
    expect(scope.endRow(8)).toBe(true);
  });
  
  it('endRow should be able to identify a cell not being the end of a row of cells', function () {
    expect(scope.endRow(0)).toBe(false);
    expect(scope.endRow(1)).toBe(false);
    expect(scope.endRow(6)).toBe(false);
  });
});
