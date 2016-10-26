var scoreCtrl = mainModule.controller('ScoreCtrl', function ($scope, scoreFactory) {
    
    //Simple controller for displaying the scores in the navigation bar
    $scope.getScore = function( index ){
        return scoreFactory.getScore( scoreFactory.playerIndex [ index ] );
    }
    
});

mainModule.factory('scoreFactory', function() {
    
    //This factory keeps track of the scores as the player plays
    var score = {};
    score.scores = { "humans" : 0, "computer" : 0,  "ties" : 0 };
    score.playerIndex = [ "humans", "computer", "ties" ];
    
    score.getScore = function( playerType ){
        return score.scores [ playerType ];
    }
    
    score.raiseScore = function ( playerType ){
        score.scores [ playerType ] ++;
    }
    
    return score;
});