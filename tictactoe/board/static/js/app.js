/** @jsx React.DOM */
var data = [0, 1, 5, 6, 4, 3, 8];

var TicTacToeCell = React.createClass({
  render: function() {
    return (
      <div className="cell">
        <span>{this.props.type}</span>
      </div>
    )
  }
});

var TicTacToeBoard = React.createClass({
  render: function() {
    var board = {};
    for (var i=0; i < this.props.data.length; i++) {
      var pos = this.props.data[i];
      var token = i % 2 ? 'O' : 'X';
      board[pos] = token;
    }
    var board_array = [];
    for (var i=0; i < 9; i++) {
      var token = board[i] || " ";
      board_array.push(token);
    }
    var cells = board_array.map(function(cell) {
      return <TicTacToeCell type={cell} />
    });
      
    return (
      <div id="board">
        {cells}
      </div>
    )
  }
});

React.renderComponent(
  <TicTacToeBoard data={data}/>,
  document.getElementById('board')
);

