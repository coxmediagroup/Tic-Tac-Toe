/* services.js */
angular.module("ticTacToeApp").factory('ai', function(){
	var LINE_INDEXES = [
		[0,1,2],[3,4,5],[6,7,8],
		[0,3,6],[1,4,7],[2,5,8],
		[0,4,8],[2,4,6]
	];

	var availableIndex = function(state, indexes){
			var index = null;
			if(state[indexes[0]] === ""){
				index = indexes[0];
			} else if(state[indexes[1]] === ""){
				index = indexes[1];
			} else {
				index = indexes[2];
			}
			return index;
	};

	lineOppScore = function(state, indexes){
		var score = 0;
		if(state[indexes[0]] === "o" || state[indexes[1]] === "o" || state[indexes[2]] === "o"){
			score = -1; // nothing to see here
		} else {
			if(state[indexes[0]] === "x"){
				score++; 
			} 
			if(state[indexes[1]] === "x"){
				score++; 
			} 
			if(state[indexes[2]] === "x"){
				score++; 
			}
		}
		return score;
	};

	getNextPosition = function(state){
		var nextPosition = -1;
		for(var i = 0; i < LINE_INDEXES.length; i++){
			if(lineOppScore(state,LINE_INDEXES[i]) > 1){
				nextPosition = availableIndex(state,LINE_INDEXES[i]);
				break;
			}
		}
		if(nextPosition === -1){
			/* 
			This takes the first available spot it should find the first
			spot where a win is possible.
			*/
			for(var i = 0; i < 9; i++){
				if(state[i] === ''){
					nextPosition = i;	
				}
			}
		}
		return nextPosition;
	}

	var ai = {};
	ai.turn = function(state){
		/* 
			Determines what turn it is based on the state:
			0,1 = turn 1
			2,3 = turn 3
			4,5 = turn 5
			6,7 = turn 7
			8,9 = turn 9 - game over
		*/
		var turn = 1;
		var pickedCount = 0;
		for(var i = 0; i < state.length; i++){
			if(state[i] !== ''){
				pickedCount++;
			} 
		}

		if(pickedCount < 2){
			turn = 1;
		} else if(pickedCount < 4){
			turn = 3;
		} else if(pickedCount < 6){
			turn = 5;
		} else if(pickedCount < 8){
			turn = 7;
		} else {
			turn = 9;
		}
		return turn;
	};
	ai.nextPlay = function(state){
		var nextPosition = 0;
		if(this.turn(state) === 1){
			if(state[4] === ''){
				nextPosition = 4;
			} else {
				nextPosition = 0;
			}
		} else if(this.turn(state) === 3){
			nextPosition = getNextPosition(state);
		} else if(this.turn(state) === 5){
			// check for win move here
			nextPosition = getNextPosition(state);
		} else if(this.turn(state) === 7){
			// check for win move here
			nextPosition = getNextPosition(state);
		} 
		return nextPosition;
	};
	return ai;
});