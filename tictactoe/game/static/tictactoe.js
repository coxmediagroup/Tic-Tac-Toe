window.onload = function() {

    var gameboard = document.getElementById('gameboard')

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
}//window.onload




