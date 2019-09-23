import React, { Component } from 'react'
import axios from 'axios'
import Main from '../templates/Main'

const headerProps = {
    icon: 'home',
    title: 'Início',
    subtitle: 'Bem vindo a sessão de administrador'
}

const baseUrl = 'http://localhost:5000/usuario'
const initialState = {
    user: { name: '', email: '' },
    usuariosVagas: []
}

export default class AdminInicio extends Component {

    state = { ...initialState }

    componentWillMount() {
        const url = baseUrl + 's/vagas'
        axios(url).then(resp => {
            this.setState({ usuariosVagas: resp.data.usuarios })
        })
    }

    renderTable() {
        return (
            <table className="table mt-4">
                <thead>
                    <tr>
                        <th>Vaga</th>
                        <th>Tipo</th>
                        <th>Proprietário</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderRows()}
                </tbody>
            </table>
        )
    }

    renderRows() {
        var exib = []
        this.state.usuariosVagas.map(usr => {
            usr.vagas.map(vg => {
                exib.push({
                    usrId: usr.id,
                    vaga: vg.identificador,
                    tipoVaga: vg.tipo,
                    proprietario: usr.nome + ' ' + usr.sobrenome,
                    status: vg.estado,
                })
            })
        })

        return exib.map(exb => {
            return (
                <tr key={exb.usrId}>
                    <td>{exb.vaga}</td>
                    <td>{exb.tipoVaga}</td>
                    <td>{exb.proprietario}</td>
                    <td>{exb.status}</td>
                </tr>
            )
        })
    }

    render() {
        return (
            <Main {...headerProps}>
                {this.renderTable()}
            </Main>
        )
    }
}