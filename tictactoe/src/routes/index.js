import React from 'react'
import {Route, IndexRoute} from 'react-router'
import Template from '../containers/Template.js'
import Home from '../containers/Home'
import Profile from '../containers/Profile'

const createRoutes = () => {
  return (
    <Route
      path='/'
      component={Template}
    >
      <IndexRoute
        component={Home}
      >
      </IndexRoute>


      <Route
        path={'/profile'}
        component={Profile}
      >
      </Route>
    </Route>
  )
}

const Routes = createRoutes()

export default Routes
