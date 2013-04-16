/* --- Marker class --- */

marker = function() {
    var self = this;
    self.player = ko.observable('');
    self.chosen = ko.observable(false);

    self.choose = function(isHuman) {
        if( !this.chosen()) {
            whichPlayer = isHuman ? 'X' : 'O';
            self.player(whichPlayer);
            self.chosen(true);
            return true;
        } else {
            return false;
        }
    };
};

/* --- Main view --- */

viewModel = function() {
    var self = this;
    self.markers = ko.observableArray(); // Our collection of marker objects will be stored here.
    self.gameInProgress = ko.observable(false);
    self.gameIsOver = ko.observable(false);
    self.canPlaceMarker = ko.observable(true);
    
    self.chooseMarker = function(marker) {
        if( self.canPlaceMarker()) {
            self.gameInProgress(true);
            self.canPlaceMarker(false);
            if( marker.choose(true)) {
                self.getAIMove();
            } else {
                toastr.error('The tile you chose already contains a marker.');
            }
            self.canPlaceMarker(true);
        } else {
            toastr.warning('Wait for AI to make its move.');
        }
    };
    
    self.getAIMove = function() {
        // One step at a time... UI, then AI. :)
        /*self.canPlaceMarker(false);
        $.ajax({
            url: '',
            type: 'POST',
            data: ko.toJSON(self.markers),
            success: function(data) {
                dataParsed = $.parseJSON(data);
                // We have a winner! End game and display notification.
                if( dataParsed.gameOver ) {
                    self.gameIsOver(true);
                    switch(dataParsed.winner) {
                        case 'X':
                            toastr.success('You won... but HOW??'); // Inconceivable!
                            break;
                        case 'O':
                            toastr.success('AI has won the game.');
                            break;
                        default:
                            toastr.info('The game has ended in a draw.');
                            break;
                    }
                } else {
                    // No winner, so place marker chosen by AI.
                    self.markers()[dataParsed.AIMarker].choose();
                }
            }
        });*/
    };
    
    self.requestReset = function() {
        // If there is a game in progress, prompt user to confirm their intentions to restart.
        if( !self.gameIsOver()) {
            $('#resetConfirmationModal').modal('show');
        } else {
            self.initializeGame();
        }
    };
    
    self.initializeGame = function() {
        self.markers.removeAll();
        self.gameInProgress(false);
        self.gameIsOver(false);

        // Push 9 new markers into markers observable array, to represent our game matrix.
        for( i=0; i<9; i++ ) {
            self.markers.push(new marker());
        }
        
    };  
};

/* --- Fire it up, once all assets have come down the pipe! --- */

$(document).ready( function() {
    ticTacToe = new viewModel();
    ko.applyBindings(ticTacToe);
    ticTacToe.initializeGame();
});
