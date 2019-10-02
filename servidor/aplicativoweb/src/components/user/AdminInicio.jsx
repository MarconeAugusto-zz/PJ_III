import React, { Component } from 'react'
import axios from 'axios'
import Main from '../templates/Main'
import './AdminInicio.css'

const headerProps = {
    icon: 'home',
    title: 'Início',
    subtitle: 'Bem vindo a sessão de administrador'
}

const baseUrl = 'http://localhost:5000/'
const initialState = {
    vagas: [],
    usuariosVagas: [],
    eventos: []
}

export default class AdminInicio extends Component {

    state = { ...initialState }

    componentWillMount() {
        let url = baseUrl + 'vaga'
        axios(url).then(resp => {
            this.setState({ vagas: resp.data.vagas })
        })

        url = baseUrl + 'usuarios/vagas'
        axios(url).then(resp => {
            this.setState({ usuariosVagas: resp.data.usuarios })
        })

        url = baseUrl + 'eventos'
        axios(url, {
            params: {
                limit: 20
            }
        }).then(resp => {
            this.setState({ eventos: resp.data })
        })
        // this.state.vagas.forEach(v => {
        //     const k = v
        //     const chave = k.identificador
        //     // delete k.identificador
        //     this.setState({ chave: k })
        // }) 
    }

    renderTableVagas() {
        return (
            <table className="table table-bordered table-hover-my mt-6">
                <tbody>
                    {this.renderRowsVagas()}
                </tbody>
            </table>
        )
    }

    getCellToolTip(estadoVaga) {
        switch (estadoVaga) {
            case 1:
                return 'Livre Autenticação OK'
            case 2:
                return 'Livre Autenticação Não OK'
            case 3:
                return 'Ocupado Autenticação OK'
            case 4:
                return 'Ocupado Autenticação Não OK'
            default:
                return 'Estado indefinido'
        }
    }

    renderRowsVagas() {
        const countVagas = this.state.vagas.length
        let linhas = Math.round(Math.sqrt(countVagas))
        let colunas = linhas
        if (linhas*colunas < countVagas)
            colunas += 1
        
        let elementos = linhas*colunas
        let linhasTabela = []
        for(let i=0;i<countVagas;i=i+colunas) {
            linhasTabela.push(this.state.vagas.slice(i, i+colunas))
        }
        
        return linhasTabela.map((row, i) => {
            return (
                <tr key={i}>
                    {row.map((col, j) =>
                        <td key={j} className={'status-vaga-' + col.estado} align="center"
                            data-toggle="tooltip" data-placement="top" title={this.getCellToolTip(col.estado)}>
                            {col.identificador}
                            </td>
                    )}
                </tr>
            )
        })
    }

    renderTableEventos() {
        return (
            <table className="table mt-4">
                <thead>
                    <tr>
                        <th>Vaga</th>
                        <th>Evento</th>
                        <th>Data</th>
                    </tr>
                </thead>
                <tbody>
                    {this.renderEventosRows()}
                </tbody>
            </table>
        )
    }

    renderEventosRows() {
        return this.state.eventos.map(evento => {
            return (
                <tr key={evento.identificadorVaga}>
                    <td>{evento.identificadorVaga}</td>
                    <td>{evento.tipo}</td>
                    <td>{evento.data}</td>
                </tr>
            )
        })
    }

    render() {
        return (
            <Main {...headerProps}>
                <h2>Estados das Vagas</h2>
                {this.renderTableVagas()}
                <br></br>
                <h2>Últimos eventos</h2>
                {this.renderTableEventos()}
            </Main>
        )
    }
}