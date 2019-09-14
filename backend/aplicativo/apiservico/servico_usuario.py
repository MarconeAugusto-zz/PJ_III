import sys

from entidades.usuario import Usuario
from entidades.base import Session, engine, Base

class ServicoUsuario(object):
    def obtem(self, idUsuario=None):
        session = Session()
        usuarios = None

        if idUsuario is not None:
            usuarios = session.query(Usuario).filter(Usuario.id == idUsuario).first()
        else:
            usuarios = session.query(Usuario).all()

        session.close()

        usuariosJson = [usr.converteParaJson() for usr in usuarios] if usuarios is not None else None
        return usuariosJson

    def novoUsuarioDadosValidados(self, dados):
        dadosObrigatorios = ['nome', 'sobrenome', 'login', 'senha', 'tipo']
        return all(dado in dados for dado in dadosObrigatorios)

    def adiciona(self, dados):
        if not self.novoUsuarioDadosValidados(dados):
            # Faltando parametros.. retorna um erro
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        usuario = Usuario(dados['nome'], dados['sobrenome'], dados['login'], dados['senha'], dados['tipo'])

        session = Session()
        try:
            session.add(usuario)
            session.commit()
        except Exception as e:
            return {'erro': 500, 'msg': 'Erro ao adicionar usuario', 'exc': str(e)}
        finally:
            session.close()
        
        return {'msg': 'Usuario adicionado'}


servicoUsuario = ServicoUsuario()