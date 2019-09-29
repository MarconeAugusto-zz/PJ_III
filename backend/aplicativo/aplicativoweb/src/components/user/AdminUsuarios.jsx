import React, { Component } from 'react'
import axios from 'axios'
import Main from '../templates/Main'

const headerProps = {
    icon: 'users',
    title: 'Usuários',
    subtitle: 'Cadastro de usuários: Incluir, Listar, Alterar e Excluir!'
}

const baseUrl = 'http://localhost:5000/usuario'
const initialState = {
    user: { nome: '', sobrenome: '', login: '', senha: '', senha_c: '', tipo: '', tipo_str: ''},
    usuarios: []
}

export default class AdminUsuarios extends Component {
    state = { ...initialState }

    componentWillMount() {
        axios(baseUrl).then(resp => {
            this.setState({ usuarios: resp.data.usuarios })
        })
    }

    clear() {
        this.setState({user: initialState.user})
    }

    save() {
        const user = this.state.user
        if (user.tipo_str === 'Administrador')
            user.tipo = 1
        else
            user.tipo = 2
            
        if (user.senha !== user.senha_c) {
            console.log("Senha confirmada errada")
            return
        }

        console.log(user)
        const method = user.id ? 'put' : 'post'
        const url = user.id ? `${baseUrl}/${user.id}` : baseUrl
        axios[method](url, user)
            .then(resp => {
                const usuarios = this.getUpdatedList(resp.data.usuario)
                this.setState({ user: initialState.user, usuarios })
            })
        console.log(this.state.usuarios)
    }

    getUpdatedList(user, add = true) {
        const list = this.state.usuarios.filter(u => u.id !== user.id)
        if (add) list.unshift(user)
        // list.unshift(user) // poe na primeira posicao do array
        return list
    }

    updateField(event) {
        // nao é interessante alterar diretamente o state
        // pois pra isso existe a funcao setState
        // desta forma, vamos criar uma cópia através do operador spread
        const user = { ...this.state.user }
        user[event.target.name] = event.target.value
        this.setState({user})
    }

    renderDropdownTipoUsuario(){
        return (
        <div class="col-12 col-md-6">
            <div class="form-group">
                <label for="tipo">Tipo</label>
                <select value={this.state.user.tipo_str} onChange={e => this.updateField(e)} name="tipo_str" class="form-control">
                    <option>Selecione</option>
                    <option value="Administrador">Administrador</option>
                    <option value="Usuario">Usuario</option>
                </select>
            </div>
        </div>
        )
      }

    renderForm() {
        return (
            <div className="form">
                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Nome</label>
                            <input type="text" className="form-control"
                                name="nome"
                                value={this.state.user.nome}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o nome ..." />
                        </div>
                    </div>

                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Sobrenome</label>
                            <input type="text" className="form-control"
                                name="sobrenome"
                                value={this.state.user.sobrenome}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o sobrenome ..." />
                        </div>
                    </div>

                </div>

                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Login</label>
                            <input type="text" className="form-control"
                                name="login"
                                value={this.state.user.login}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite o login ... " />
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Senha</label>
                            <input type="password" className="form-control"
                                name="senha"
                                value={this.state.user.senha}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite a senha ..." />
                        </div>
                    </div>

                    <div className="col-12 col-md-6">
                        <div className="form-group">
                            <label>Confirme a Senha</label>
                            <input type="password" className="form-control"
                                name="senha_c"
                                value={this.state.user.senha_c}
                                onChange={e => this.updateField(e)}
                                placeholder="Digite a senha ..." />
                        </div>
                    </div>

                    {this.renderDropdownTipoUsuario()}


                </div>

                <hr />

                <div className="row">
                    <div className="col-12 d-flex justify-content-end">
                        <button className="btn btn-primary"
                            onClick={e => this.save(e)}>
                            Salvar
                        </button>
                        <button className="btn btn-secondary ml-2"
                            onClick={e => this.clear(e)}>
                            Cancelar
                        </button>
                    </div>
                </div>

            </div>
        )
    }

    load(user) {
        user.senha = ""
        user.senha_c = ""
        console.log(user)
        this.setState({ user })
    }

    remove(user) {
        axios.delete(`${baseUrl}/${user.id}`).then(resp => {
            const usuarios = this.getUpdatedList(user, false)
            this.setState({ usuarios })
        })
    }

    renderTable() {
        return (
            <table className="table mt-4">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Sobrenome</th>
                        <th>Login</th>
                        <th>Tipo</th>
                        <th>Data de Cadastro</th>
                        <th>*</th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderRows()}
                </tbody>
            </table>
        )
    }

    renderRows() {
        return this.state.usuarios.map(user => {
            return (
                <tr key={user.id}>
                    <td>{user.nome}</td>
                    <td>{user.sobrenome}</td>
                    <td>{user.login}</td>
                    <td>{user.tipo_str}</td>
                    <td>{user.dataCadastro}</td>
                    <td>
                        <button className="btn btn-warning"
                            onClick={() => this.load(user)}>
                            <i className="fa fa-pencil"></i>
                        </button>
                        <button className="btn btn-danger ml-2"
                            onClick={() => this.remove(user)}>
                            <i className="fa fa-trash"></i>
                        </button>
                    </td>

                </tr>
            )
        })
    }

    render() {
        return (
            <Main {...headerProps}>
                {this.renderForm()}
                {this.renderTable()}
            </Main>
        )
    }
}