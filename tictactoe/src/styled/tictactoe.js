import React from 'react'
import {Layer, Line} from 'react-konva'

export const Board = ({unit, size, rows}) => {
let grid = []
let stroke = 'grey'
let strokeWidth = 10

for (let i = 1; i < rows; i++){
  let position  = unit * i
  grid.push(
    <Line
      points={[position, 0, position, size ]}
      stroke={stroke}
      strokeWidth={strokeWidth}
      key={i+'y'}
    />
  )
  grid.push(
    <Line
      points={[0, position, size, position ]}
      stroke={stroke}
      strokeWidth={strokeWidth}
      key={i+'x'}
    />
  )
}

  return (
    <Layer>
      {grid}
    </Layer>
  )
}
