import React from 'react'
import { Switch, Route, Redirect } from 'react-router'

import UserCrud from '../user/UserCrud'
import PaginaLogin from '../login/PaginaLogin'
import AdminInicio from '../user/AdminInicio'

export default props =>
    <Switch>
        <Route exact path='/' component={AdminInicio} />
        <Route path='/users' component={UserCrud} />
        <Redirect from='*' to='/' />
    </Switch>