/* services.js */
angular.module("ticTacToeApp").factory('ai', function(){
	var LINE_INDEXES = [
		[0,1,2],[3,4,5],[6,7,8],
		[0,3,6],[1,4,7],[2,5,8],
		[0,4,8],[2,4,6]
	];

	var won = false;
	var tie = false;

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

	var negativeScore = function(state, indexes, side){
		var score = 0;
		if(state[indexes[0]] === side || state[indexes[1]] === side || state[indexes[2]] === side){
			score = -1; // nothing to see here
		}
		return score;		
	};

	var positiveScore = function(state, indexes, side){
		var score = 0;
		if(state[indexes[0]] === side){
			score++; 
		} 
		if(state[indexes[1]] === side){
			score++; 
		} 
		if(state[indexes[2]] === side){
			score++; 
		}
		return score;		
	};

	var lineOppScore = function(state, indexes){
		var score = negativeScore(state, indexes, "o");
		if(score === 0){
			score = positiveScore(state, indexes, "x");
		}
		return score;
	};

	var lineMyScore = function(state, indexes){
		var score = negativeScore(state, indexes, "x");
		if(score === 0){
			score = positiveScore(state, indexes, "o");
		}
		return score;
	};

	var getNextPosition = function(state){
		var nextPosition = -1;
		var bestScore = {index:-1,score:-2};
		var score = 0;
		// score the lines
		for(var i = 0; i < LINE_INDEXES.length; i++){
			score = lineMyScore(state,LINE_INDEXES[i]);
			if(score > bestScore.score){
				bestScore.index = i;
				bestScore.score = score;
			}
		}
		// first  check for a possible win
		if(bestScore.score == 2){ 
			nextPosition = availableIndex(state, LINE_INDEXES[bestScore.index]);
			won = true;
		}
		// second block a win
		if(nextPosition === -1){  // i don't have a winning move
			for(var i = 0; i < LINE_INDEXES.length; i++){
				if(lineOppScore(state,LINE_INDEXES[i]) > 1){
					nextPosition = availableIndex(state,LINE_INDEXES[i]);
					break;
				}
			}
		}
		// if I can't win and I don't need to block...
		if(nextPosition === -1){  // they don't have a winning move
			if(bestScore.score === -1){ // no possible victory for either side
				for(var i = 0; i < state.length; i++){
					if(state[i] === ''){
						nextPosition = i; 
						break;
					}
				}
			} else {
				nextPosition = availableIndex(state, LINE_INDEXES[bestScore.index]);
			}
		
		}
		return nextPosition;
	};

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
			if(state[4] === "x" && state[8] === "x"){
				nextPosition = 2; // special case
			} else {
				nextPosition = getNextPosition(state);				
			}
		} else if(this.turn(state) === 5){
			nextPosition = getNextPosition(state);
		} else if(this.turn(state) === 7){
			nextPosition = getNextPosition(state);
		} else {
			if(!won) tie = true;
		}
		return nextPosition;
	};
	ai.reset = function(){
		won = false;
		tie = false;
	};
	ai.hasWon = function(){
		return won;
	};
	ai.hasTied = function(){
		return tie;
	};
	return ai;
});