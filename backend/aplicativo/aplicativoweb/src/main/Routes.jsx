import React from 'react'
import { Switch, Route, Redirect } from 'react-router'

import Home from '../components/home/Home'
import HomeAdmin from '../components/home/HomeAdmin'
import UserCrud from '../components/user/UserCrud'
import PaginaLogin from '../components/login/PaginaLogin'

export default props =>
    <Switch>
        <Route exact path='/' component={PaginaLogin} />
        <Route path='/users' component={UserCrud} />
        <Route path='/login' component={PaginaLogin} />
        {/* <Route path='/home' component={Home} /> */}
        <Route path='/HomeAdmin' component={HomeAdmin} />
        {/* <Redirect from='*' to='/' /> */}
    </Switch>