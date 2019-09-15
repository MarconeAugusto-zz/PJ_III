from entidades.vaga import Vaga
from entidades.usuario import Usuario
from entidades.base import Session

class ServicoVaga(object):
    def obtem(self, idVaga=None):
        session = Session()
        vaga = None

        if idVaga is not None:
            vagas = session.query(Vaga).filter(Vaga.id == idVaga).first()
        else:
            vagas = session.query(Vaga).all()

        session.close()

        vagasJson = None
        if vagas is not None:
            if type(vagas) == list:
                vagasJson = [vg.converteParaJson() for vg in vagas]
            else:
                vagasJson = vagas.converteParaJson()

        return vagasJson

    def novaVagaDadosValidados(self, dados):
        dadosObrigatorios = ['identificador', 'codigo']
        return all(dado in dados for dado in dadosObrigatorios)

    def _atrela_usuario_vaga(self, vaga, idUsuario, sessao):
        usuario = sessao.query(Usuario).filter(Usuario.id == idUsuario).first()
        if usuario is None:
            return

        usuario.setaVagas(vaga)

    def adiciona(self, dados):
        if not self.novaVagaDadosValidados(dados):
            # Faltando parametros.. retorna um erro
            return {'erro': 400, 'msg': 'Parametros incompletos'}

        vaga = Vaga(dados['identificador'], dados['codigo'])
        if 'estado' in dados:
            vaga.setaEstado(dados['estado'])

        if 'tipo' in dados:
            vaga.setaTipo(dados['tipo'])

        session = Session()
        try:
            session.add(vaga)

            if 'idUsuario' in dados:
                self._atrela_usuario_vaga(vaga, dados['idUsuario'], session)

            session.commit()

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao adicionar usuario'}
        finally:
            session.close()
        
        return {'msg': 'Vaga adicionada'}


servicoVaga = ServicoVaga()