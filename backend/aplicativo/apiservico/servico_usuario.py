from entidades.usuario import Usuario
from entidades.base import Session

class ServicoUsuario(object):
    def obtem(self, idUsuario=None, comVagas=False):
        session = Session()
        usuarios = None

        if idUsuario is not None:
            usuarios = session.query(Usuario).filter(Usuario.id == idUsuario).first()
        else:
            usuarios = session.query(Usuario).all()

        usuariosJson = None
        if usuarios is not None:
            if type(usuarios) == list:
                usuariosJson = [usr.converteParaJson(comVagas) for usr in usuarios]
            else:
                usuariosJson = usuarios.converteParaJson(comVagas)

        session.close()
        return usuariosJson

    def novoUsuarioDadosValidados(self, dados):
        dadosObrigatorios = ['nome', 'sobrenome', 'login', 'senha', 'tipo']
        return all(dado in dados for dado in dadosObrigatorios)

    def adiciona(self, dados):
        if not self.novoUsuarioDadosValidados(dados):
            # Faltando parametros.. retorna um erro
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        usuario = Usuario(dados['nome'], dados['sobrenome'], dados['login'], dados['senha'], dados['tipo'])
        usuarioJson = {}

        session = Session()
        try:
            session.add(usuario)
            session.commit()
            usuarioJson = usuario.converteParaJson()
        except Exception as e:
            return {'erro': 500, 'msg': 'Erro ao adicionar usuario', 'exc': str(e)}
        finally:
            session.close()
        
        return {'msg': 'Usuario adicionado', 'usuario': usuarioJson}

    def _obtemUsuarioPorId(self, sessao, idUsuario):
        usuario = sessao.query(Usuario).filter(Usuario.id == idUsuario).first()
        return usuario

    def obtemVagas(self, idUsuario):
        sessao = Session()

        usuario = self._obtemUsuarioPorId(sessao, idUsuario)
        if usuario is None:
            sessao.close()
            return {'erro': 404, 'msg': 'Usuario nao encontrado'}
        
        vagas = usuario.obtemVagas()
        sessao.close()
        vagasJson = [vg.converteParaJson() for vg in vagas]
        return vagasJson

    def removeUsuario(self, idUsuario):
        usuarioJson = {}
        session = Session()
        try:
            usuario = session.query(Usuario).filter(Usuario.id == idUsuario).first()

            if usuario is None:
                return {'erro': 404, 'msg': 'Usuario nao encontrado'}

            usuarioJson = usuario.converteParaJson()
            session.delete(usuario)
            session.commit()
        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao remover usuario', 'exc': str(e)}
        finally:
            session.close()
        
        return {'msg': 'Usuario removido', 'usuario': usuarioJson}



servicoUsuario = ServicoUsuario()