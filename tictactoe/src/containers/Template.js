import React, {Component} from 'react'
// import ReactDOM from 'react-dom'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import injectTapEnventPlugin from 'react-tap-event-plugin'
import RaisedButton from 'material-ui/RaisedButton'
import {Stage} from 'react-konva'
import {Board, Squares} from '../styled/tictactoe'

injectTapEnventPlugin()

class Template extends Component {

  constructor(props) {
    super(props)
    this.combos = [
      [0,1,2],
      [3,4,5],
      [6,7,8],
      [0,3,6],
      [1,4,7],
      [2,5,8],
      [0,4,8],
      [2,4,6]
    ]
  }

  state = {
    rows: 3,
    gameState: new Array(9).fill(false),
    ownMark: 'X',
    otherMark: 'O',
    gameOver: false,
    yourTurn: true,
    winner: false,
    win: false
  }

  componentWillMount() {
    let height = window.innerHeight
    let width = window.innerWidth
    let size = (height < width) ? height * .8 : width * .8
    let rows = this.state.rows
    let unit = size / rows
    let coordinates = []
    for (let y = 0; y < rows; y++){
      for (let x = 0; x < rows; x++){
        coordinates.push([x*unit, y*unit])
      }
    }

    this.setState({
      size,
      rows,
      unit,
      coordinates
    })
  }

  chooseO = (index, marker) => {
    this.setState( (chooseMark, prop) => {
      let {ownMark, otherMark} = chooseMark
      ownMark = 'O'
      otherMark = 'X'
      return{
        ownMark: 'O' ,
        otherMark: 'X'
      }
    })
  }

  chooseX = (index, marker) => {
    this.setState( (chooseMark, prop) => {
      let {ownMark, otherMark} = chooseMark
      ownMark = 'X'
      otherMark = 'O'
      return{
        ownMark: 'X' ,
        otherMark: 'O'
      }
    })
  }

  resetButton = (index, marker) => {
    let openSquares = []

    this.setState( (chooseReset, prop) => {
      let {gameState} = chooseReset
      let openSquares = []
      if (openSquares.length === 0){
       return{
       gameState: new Array(9).fill(false)
     }
   }
  })
}


  // this.chooseX = (index, marker) => {
  //   this.state.ownMark = 'X'
  //   this.state.otherMark = 'O'
  // }

  move = (index, marker) => {
    this.setState( (prevState, prop) => {
        let {gameState, yourTurn, gameOver, winner} = prevState
        yourTurn = !yourTurn
        gameState.splice(index, 1, marker)
        let foundWin = this.checkWin(gameState)
        if (foundWin) {
          winner = gameState[foundWin[0]]
        }
        if(foundWin || !gameState.includes(false)) {
          gameOver = true
        }
        if (!yourTurn && !gameOver){
          this.makeAiMove(gameState)
        }
        return {
          gameState,
          yourTurn,
          gameOver,
          win: foundWin || false,
          winner
        }
      })
    }

  makeAiMove = (gameState) => {

    // let bestMoveScore = 100;
    let otherMark = this.state.otherMark
    let openSquares = []
    // let score = null

    gameState.forEach( (square, index)=> {
      if(!square) {
        openSquares.push(index)
      }
    })

    let aiMove = openSquares[this.random(0, openSquares.length)]
    setTimeout(()=>{
      this.move(aiMove, otherMark)
    })

//minimax loop function
    // for (var i = 0; i < openSquares.length; i++){
    //   let newGameState = this.move(i, otherMark);
    //   if (newGameState){
    //     var moveScore = this.maxScore(newGameState);
    //     if(moveScore < bestMoveScore){
    //       bestMoveScore = moveScore;
    //       score = i;
    //     }
    //   }
    // }
    //
    // return score;
  }

  random = (min, max) => {
    min = Math.ceil(min)
    max = Math.floor(max)
    return Math.floor(Math.random() * (max-min)) + min
  }

  checkWin = (gameState) => {
    let combos = this.combos
    return combos.find( (combo) => {
      let [a,b,c] = combo
      return (gameState[a] === gameState[b] && gameState[a] === gameState[c] && gameState[a])
    })
  }

//beginning of minimax function

  // winner = (gameState) => {

  //   let player = this.state.ownMark || this.state.otherMark;
  //   if(
  //     gameState[0] === player && gameState[1] === player && gameState[2] === player ||
  //     gameState[3] === player && gameState[4] === player && gameState[5] === player ||
  //     gameState[6] === player && gameState[7] === player && gameState[8] === player ||
  //     gameState[0] === player && gameState[3] === player && gameState[6] === player ||
  //     gameState[1] === player && gameState[4] === player && gameState[7] === player ||
  //     gameState[2] === player && gameState[5] === player && gameState[8] === player ||
  //     gameState[0] === player && gameState[4] === player && gameState[8] === player ||
  //     gameState[2] === player && gameState[4] === player && gameState[6] === player
  //   ){
  //     return true;
  //   } else {
  //     return false;
  //   }
  // }

  // copyGameState = (gameState, index, marker) => {
  //   return gameState
  //   return gameState.splice(index, 1, marker)
  //   let {gameState, yourTurn, gameOver, winner} = prevState
  // }
  //
  // validMove(move, mark, gameState){
  //
  //   let combo = this.combos
  //   let [a,b,c] = combo
  //
  //   let newGameState = this.copyGameState(gameState);
  //   if (newGameState[move] === (gameState[a] === gameState[b] && gameState[a] === gameState[c] && gameState[a])){
  //     newGameState[move] = mark;
  //     return newGameState;
  //   }
  // }

  // findAiMove = (gameState) => {
  //   let move = null
  //   let otherMark = this.state.otherMark;
  //   let ownMark = this.state.ownMark;
  //   let openSquares = [];
  //   let bestMoveScore = 100;
  //   if(this.checkWin(gameState, ownMark) || this.checkWin(gameState, otherMark) || this.tie(gameState)){
  //     return false;
  //   }
  //   for (var i = 0; i < openSquares.length; i++){
  //     let newBoard = this.validMove(i, this.state.otherMark, gameState);
  //     if(newBoard) {
  //       let moveScore = this.maxScore(newBoard);
  //       if(moveScore < bestMoveScore) {
  //         bestMoveScore = moveScore;
  //          move = i;
  //       }
  //     }
  //   }
  //   return move;
  // }

  tie(gameState){
    let openSquares = []
    // var move = combos.join(combos).replace('');
    if (openSquares.length === 0) {
      return true;
    }
    return false;
  }

  // minimax(index, gamestate){
  //   let openSquares = [];
  //
  //   if(this.move(gameState, ownMark)){
  //     return {score:10};
  //   } else if (this.move(gameState, otherMark)) {
  //     return {score:-10};
  //   } else if (openSquares.length === 0){
  //     return {score:0};
  //   }
  //
  //
  //
  //   for (var i = 0; i < openSquares.length; i++){
  //     var moveScore = {score};
  //
  //
  //     moveScore.index =
  //     let newGameState = this.move(i, marker);
  //
  //     if (marker === otherMark){
  //       var moveScore = minimax(index, ownMark)
  //     }
  //
  //
  //     if (newGameState){
  //       var moveScore = minimax(index, gamestate);
  //       if(moveScore < bestMoveScore){
  //         bestMoveScore = moveScore;
  //         score = i;
  //       }
  //     }
  //   }
  //
  // }

  minScore(gameState) {
    let openSquares = [];
    let otherMark = this.state.otherMark;
    let ownMark = this.state.ownMark;

    if(this.move(gameState, ownMark)){
      return 10;
    } else if (this.move(gameState, otherMark)) {
      return -10;
    } else if (openSquares.length === 0){
      return 0;
    } else {
      let bestMoveValue = 100;
      for(var i = 0; i < openSquares.length; i++){
        let newGameState = this.move(i, otherMark);
        if(newGameState){
          let predictedMoveValue = this.maxScore(newGameState);
          if(predictedMoveValue < bestMoveValue){
            bestMoveValue = predictedMoveValue;
          }
        }
      }
      return bestMoveValue;
    }
  }

  maxScore(gameState) {
    let openSquares = [];
    let otherMark = this.state.otherMark;
    let ownMark = this.state.ownMark;

    if(this.move(gameState, ownMark)){
      return 10;
    } else if (this.move(gameState, otherMark)) {
      return -10;
    } else if (openSquares.length === 0){
      return 0;
    } else {
      let bestMoveValue = -100;
      for(var i = 0; i < openSquares.length; i++){
        let newGameState = this.move(i, ownMark);
        if(newGameState){
          let predictedMoveValue = this.maxScore(newGameState);
          if(predictedMoveValue > bestMoveValue){
            bestMoveValue = predictedMoveValue;
          }
        }
      }
      return bestMoveValue;
    }
  }

// gameLoop(index){
//   if(this.move(index, marker)){
//     this.setState({
//
//     });
//     return;
//   }
//   if(this.tie(currentGameBoard)){
//     this.setState({
//       currentGameBoard,
//       player,
//     });
//     return;
//   }
//   player = this.otherMark;
//   currentGameBoard = this.validMove(this.findAiMove(currentGameBoard), player, currentGameBoard);
//   if(this.winner(currentGameBoard, player)){
//     this.setState({
//       currentGameBoard,
//       player
//     });
//     return;
//   }
//   if(this.tie(currentGameBoard)){
//     this.setState({
//       currentGameBoard,
//       player,
//     });
//     return;
//   }
//   this.setState({
//     currentGameBoard
//   });
// }

//End of minimax function

  render() {
    let {
      size,
      unit,
      rows,
      coordinates,
      gameState,
      win,
      gameOver,
      yourTurn,
      ownMark
    } = this.state
    return (
      <MuiThemeProvider>
      <div>

        <h1>
          TicTacToe!
        </h1>

        <Stage
          width={size}
          height={size}
        >
          <Board
            unit={unit}
            rows={rows}
            size={size}
          />

          <Squares
            unit={unit}
            coordinates={coordinates}
            gameState={gameState}
            win={win}
            gameOver={gameOver}
            yourTurn={yourTurn}
            ownMark={ownMark}
            move={this.move}
          />

        </Stage>

        <RaisedButton
          label={'O'}
          primary={true}
          onTouchTap={this.chooseO}
        />

        <RaisedButton
          label={'X'}
          secondary={true}
          onTouchTap={this.chooseX}
        />

        <RaisedButton
          label={'Reset'}
          default={true}
          onTouchTap={this.resetButton}
        />

      </div>
    </MuiThemeProvider>
    )
  }
}



export default Template
