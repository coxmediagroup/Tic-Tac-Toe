/// <reference path="IObserver.ts" /> 
module TicTacToe {

	export class Observable { // or Interface 
	    private observers : IObserver [];

	    constructor() {
	        this.observers = [];
	    }

	    registerObserver (observer : IObserver) : void {
	        this.observers.push(observer);
	    }

	    removeObserver (observer : IObserver) : void {
	        this.observers.splice(this.observers.indexOf(observer), 1);
	    }

	    notifyObservers (arg : any) : void {

	        this.observers.forEach((observer : IObserver)=> {
	            observer.update(arg);
	        });
	    }
	}

}