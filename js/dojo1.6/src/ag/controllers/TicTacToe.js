dojo.require('agi.classes.Controller');
dojo.require('ag.widget.BusyOverlay');
dojo.provide('ag.controllers.TicTacToe');

dojo.declare(
    'ag.controllers.TicTacToe',
    [agi.classes.Controller],
    {
        // Controller for playing a tic tac toe game
        moveIds: ['move-1','move-2','move-3','move-4',
            'move-5','move-6','move-7','move-8','move-9'],
        theBoard: [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        connections: [],
        busyOverlay: null,
        genericErrorMessage: "There was a problem. Please try again.",
        CODE_YOU_LOSE: 1,
        CODE_YOU_TIE: 2,
        CODE_CONTINUE: 3,
        CODE_YOU_WIN: 4,
        playerLetter: 'X',
        computerLetter: 'O',

        constructor: function(params) {
            console.debug(this + '.constructor()');
            this.wireBoard();
            this.busyOverlay = new ag.widget.BusyOverlay();
        },

        // Evaluate the players current move.
        // - display the users move
        // - update the board array
        // - submit the board to the server to 
        //   get the AI's next move.
        evaluatePlayerTurn: function(e) {
            console.debug(this + ".evaluatePlayerTurn()");

            // Cover the board to protect against clicks
            // while processing player move.
            this.busyOverlay.show(dojo.byId("board"));

            var target = e.currentTarget;
            var targetId = e.currentTarget.id;
            var move = targetId.charAt(targetId.length-1);

            // Update class of selected div to display players move.
            dojo.style(targetId, "opacity", 1);

            // Disable the selected divs onclick event
            //target.onclick = null;

            // Add current move to board
            this.theBoard[parseInt(move)] = this.playerLetter;
            console.debug(this.theBoard);

            // Contact server to evaluate board
            this.makeTurnRequest();
        },

        // Evaluate the AI players current move.
        // - display the AI's move
        // - update the board array
        // - display any messages if won, tie, or lose. 
        evaluateAIPlayerTurn: function(response) {
            console.debug(this + ".evaluateAIPlayerTurn()");

            var move = response.move;
            var outcomeCode = response.outcome_code;
            var message = response.message;
            var targetId = "move-"+move;

            // Update to AI Letter O
            dojo.byId(targetId).innerHTML = 'O';

            // Update class of selected div to display AI's move.
            dojo.style(targetId, "opacity", 1);

            // Add AI  move to board
            this.theBoard[parseInt(move)] = this.computerLetter;
            console.debug(this.theBoard);

            // Disconnect click handler for AI move
            dojo.disconnect(this.connections[move-1]);

            // hide the busyOverlay
            this.busyOverlay.hide();

            // Have we reached end of game?
            switch (outcomeCode) {
                case this.CODE_YOU_WIN: {
                    dojo.forEach(this.connections, dojo.disconnect);
                    alert(message);
                    return;
                }
                case this.CODE_YOU_TIE: {
                    dojo.forEach(this.connections, dojo.disconnect);
                    alert(message);
                    return;
                }
                case this.CODE_YOU_LOSE: {
                    dojo.forEach(this.connections, dojo.disconnect);
                    alert(message);
                    return;
                }
            }

        },

        // Connect every span onclick that has an id in the moveIds array. 
        wireBoard: function() {
            console.debug(this + '.wireBoard()');

            for (var i=0;i<this.moveIds.length;i++){
                this.connectMoveId(this.moveIds[i]);
            }

            dojo.connect(dojo.byId('reset'), "onclick", this, this.reset);
        },

        // Connect click events to moveId nodes.
        // - save a handle to disconnect event after onclick.
        connectMoveId: function(nodeId) {

            // click handler will disconnect onclick
            var handle = dojo.connect(dojo.byId(nodeId), "onclick",
                            dojo.hitch(this,
                            function(e){
                                dojo.disconnect(handle);
                                this.evaluatePlayerTurn(e);
                            })
            );

            // store all connections so can disconnect onclicks for AI turns.
            this.connections.push(handle);
        },

        // Submit the board to the server
        // for evaluation by the AI.
        makeTurnRequest: function() {
            console.log(this + ".makeTurnRequest()");

            // Package up the arguments for the xhrPost
            var xhrArgs = {
                url: '/games/tictactoe/turn',
                content: {
                    'board': dojo.toJson(this.theBoard)
                },
                handleAs: "json",
                load: dojo.hitch(this, function(response) {
                    console.log('Successfull board request.');
                    console.log(response);
                    this.evaluateAIPlayerTurn(response);
                }),
                error: dojo.hitch(this, function(response) {
                    console.log('Error during board request');
                    console.log(response);
                    this.displayErrorMessage(this.genericErrorMessage);
                })
            };
            dojo.xhrPost(xhrArgs);
        },

        // Display a generic message for any errors.
        displayErrorMessage: function(message) {
            console.debug(this + ".displayErrorMessage()");

            this.busyOverlay.hide();
            alert(message);
        },

        reset: function() {
            console.debug(this + ".reset()");

            this.theBoard = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '];
            this.connections = [];
            this.wireBoard();

            dojo.query("span[id^='move-']").forEach(
                function(node, index, nodelist){
                    node.innerHTML = 'X';
                    dojo.style(node.id, "opacity", 0);
                });


        }

    }
);
