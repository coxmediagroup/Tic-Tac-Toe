/// <reference path="IObserver.ts" />
var TicTacToe;
(function (TicTacToe) {
    var Observable = (function () {
        function Observable() {
            this.observers = [];
        }
        Observable.prototype.registerObserver = function (observer) {
            this.observers.push(observer);
        };

        Observable.prototype.removeObserver = function (observer) {
            this.observers.splice(this.observers.indexOf(observer), 1);
        };

        Observable.prototype.notifyObservers = function (arg) {
            this.observers.forEach(function (observer) {
                observer.update(arg);
            });
        };
        return Observable;
    })();
    TicTacToe.Observable = Observable;
})(TicTacToe || (TicTacToe = {}));
