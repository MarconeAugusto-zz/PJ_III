import React from 'react'
import { Switch, Route, Redirect } from 'react-router'

import AdminUsuarios from '../user/AdminUsuarios'
import PaginaLogin from '../login/PaginaLogin'
import AdminInicio from '../user/AdminInicio'

export default props =>
    <Switch>
        <Route exact path='/' component={AdminInicio} />
        <Route path='/users' component={AdminUsuarios} />
        <Redirect from='*' to='/' />
    </Switch>