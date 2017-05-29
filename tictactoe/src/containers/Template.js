import React, {Component} from 'react'
// import ReactDOM from 'react-dom'
// import injectTapEnventPlugin from 'react-tap-event-plugin'
// import RaisedButton from 'material-ui/RaisedButton'
import {Stage} from 'react-konva'
import {Board, Squares} from '../styled/tictactoe'


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
    rows:3,
    gameState: new Array(9).fill(false),
    ownMark: 'X',
    otherMark: 'O',
    gameOver: false,
    yourTurn: false,
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

  move = (marker, index) => {
    console.log('Move made', marker, index)
  }

  makeAiMove = (gameState) => {
    let otherMark = this.state.otherMark
    let openSquares = []
    gameState.forEach( (square, index)=> {
      if(!squares) {
        openSquares.push(index)
      }
    })
    let aiMove = openSquares[this.random(0, openSquare.length)]
    this.move(aiMove, otherMark)
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

        {/* <RaisedButton
          label={'test button'}
          primary={true}
          onTouchTap={()=>{console.log('hello, i work')}}
        /> */}

      </div>
    )
  }
}



export default Template
