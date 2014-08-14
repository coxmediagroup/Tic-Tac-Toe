var OpenSpaces = require("./openspace");

exports.Search = function (gameBoard) {
    //we are searching for all posible moves
    //open spaces tells us how many posible moves
    var moveLocations = [[0,1],[1,0]];
    var openspaces = OpenSpaces.GetOpenSpacesCount(gameBoard);
    
    return openspaces;
}