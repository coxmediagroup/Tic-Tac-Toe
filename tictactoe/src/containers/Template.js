import React, {Component} from 'react'
// import ReactDOM from 'react-dom'
// import injectTapEnventPlugin from 'react-tap-event-plugin'
// import RaisedButton from 'material-ui/RaisedButton'
import {Stage} from 'react-konva'
import {Board} from '../styled/tictactoe'


class Template extends Component {

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

    this.setState({
      size,
      rows,
      unit
    })
  }

  move = () => {

  }

  makeAiMove = () => {

  }

  render() {
    let {
      size,
      unit,
      rows
    } =this.state
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
