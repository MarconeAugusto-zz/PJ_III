import React, { Component } from 'react'
import { Redirect } from 'react-router-dom'
import axios from 'axios'
import './PaginaLogin.css'
import logo from '../../assets/imgs/simova_logo.png'

const baseUrl = 'http://localhost:5000/login'
const initialState = {
    user: { email: '', password: '' },
}

export default class PaginaLogin extends Component {

    state = { ...initialState }

    makeLogin() {
        console.log(this.state.user.email)
        console.log(this.state.user.password)
        this.props.history.push('/HomeAdmin')
        // return <Redirect to='/HomeAdmin' />
    }

    updateField(event) {
        const user = { ...this.state.user }
        user[event.target.name] = event.target.value
        this.setState({user})
    }

    renderLogin() {
        return (
            <div className="body text-center">
                <div className="form">
                    <div className="row">
                        <img src={logo} alt="" className="mb-4" width="500" height="200" />
                    </div>
                    <div className="row">
                        <div className="form-signin">
                            <h1 className="h3 mb-3 font-weight-normal">Faça o login</h1>
                            <input type="email" className="form-control"
                                placeholder="E-mail" name="email"
                                value={this.state.user.email}
                                onChange={e => this.updateField(e)}
                                required autoFocus />
                            <input type="password" className="form-control"
                                placeholder="Senha" name="password"
                                value={this.state.user.password}
                                onChange={e => this.updateField(e)}
                                required />
                            <button className="btn btn-lg btn-primary btn-block" type="submit"
                                onClick={e => this.makeLogin(e)}>Entrar</button>
                            <p className="mt-5 mb-3 text-muted">&copy; 2019</p>
                        </div>
                    </div>
                </div>
            </div>

        )
    }

    render() {
        return (
            <main>
                {this.renderLogin()}
            </main>
        )
    }
}