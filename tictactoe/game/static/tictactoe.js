window.onload = function() {

    var gameboard = document.getElementById('gameboard')

    var newGame = document.getElementById('newgame')
    newgame.addEventListener("click", function() {
        makeNewGame()
    })

    gameboard.addEventListener("click", function(element) {
        makemove(element.target.id)
    })

    function makemove(id) {
        var move = new XMLHttpRequest()
        move.open('POST', '/playgame/')
        move.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
        move.onreadystatechange = updateBoard
        move.send(id)

        var player_square = document.getElementById(id);
        if (player_square.innerHTML == '') {
            player_square.innerHTML = 'X'
        }

        function updateBoard() {
            console.log(move.readyState)
            if (move.readyState == 4) {
                json_data = move.responseText
                console.log(json_data)
                json_data = JSON.parse(json_data)
                
                document.getElementById(json_data.move).innerHTML = 'O';
            }

        } //function updateBoard
    }// function makemove

    function makeNewGame() {
        var newgame = new XMLHttpRequest()
        newgame.open('POST', '/playgame/')
        newgame.send('makenewgame')
        newgame.onreadystatechange = makeNewGame

        function makeNewGame() {
            if (newgame.readyState == 4) {
                for (var i=0; i<=8; i++) {
                    var element = document.getElementById(i);
                    element.innerHTML = '';
                }
            }
        }
    }// function makeNewGame

}//window.onload




