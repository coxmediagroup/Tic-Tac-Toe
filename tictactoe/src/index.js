import React from 'react'
import ReactDOM from 'react-dom'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import injectTapEnventPlugin from 'react-tap-event-plugin'
import RaisedButton from 'material-ui/RaisedButton'

injectTapEnventPlugin()

// const customHistory = createBrowserHistory()

ReactDOM.render(
  <MuiThemeProvider>
    <div>
      <h1>
        Hello World!
      </h1>
      <RaisedButton
        label={'test button'}
        primary={true}
        onTouchTap={()=>{console.log('hello, i work')}}
      />
    </div>
  </MuiThemeProvider>
   ,document.getElementById('root')
)
