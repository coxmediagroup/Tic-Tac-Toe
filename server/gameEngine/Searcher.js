
function search(level) {
    var res = determine(cpuGameBoard);
    if (res == CPU) {
        return 100 - level;
    }
    else if (res == PLAYER) {
        return level - 100;
    }
    else if (res == "draw") {
        return 0;
    }

    var choose = -1000;
    var temp;

    for (var i = 0; i < cpuGameBoard.length; i++) {
        for (var j = 0; j < cpuGameBoard[i].length; j++) {
            if (cpuGameBoard[i][j] == BLANK) {
                cpuGameBoard[i][j] = cpuCurrentTurn;
                swapCPUTurn();
                blankCount--;
                temp = search(level + 1);
                swapCPUTurn();
                cpuGameBoard[i][j] = BLANK;
                blankCount++;
                if (choose == -1000) {
                    choose = temp;
                }
                else if (cpuCurrentTurn == CPU) {
                    if (temp > choose) choose = temp;
                }
                else if (cpuCurrentTurn == PLAYER) {
                    if (temp < choose) choose = temp;
                }
            }
        }
    }
    return choose;
}
