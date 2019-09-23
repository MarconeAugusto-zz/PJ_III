from entidades.vaga import Vaga
from entidades.usuario import Usuario
from entidades.evento import Evento
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

    def obtemLivres(self):
        session = Session()
        # query = (session.query(Vaga)
        #         .outerjoin(associacao_usuario_vaga, associacao_usuario_vaga.c.idUsuario == Vaga.id)
        #         .filter(associacao_usuario_vaga.c.idUsuario == None)
        # )
        # select * from vaga where id not in (select idVaga from usuario_vaga);

        # query = session.query(Vaga).filter(Vaga.id.in_(session.query(Vaga.usuario)))
        query = session.query(Vaga.id)
        vagas = query.all()
        # vagas = query.all()
        # permissions = session.query(Permission).join(Role).join(User).filter(User.username='MisterX').all()
        # vagas = session.query(Vaga).join(Usuario).filter(Vaga.idVaga=1).all()
        # vagas = Session.query(Vaga).filter(Vaga.usuario.any()).all()
        session.close()

        vagasJson = None
        if vagas is not None:
            if type(vagas) == list:
                vagasJson = [vg.converteParaJson() for vg in vagas]
            else:
                vagasJson = vagas.converteParaJson()

        return None        

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


    def obtemEventos(self, idVaga):
        session = Session()
        eventos = []
        try:
            vaga = session.query(Vaga).filter(Vaga.id == idVaga).first()
            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}
            
            for evento in vaga.eventos:
                eventos.append(evento.converteParaJson())

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao obter eventos'}
        finally:
            session.close()

        return eventos


    def adicionaEvento(self, dados):
        if 'id' not in dados or 'estado' not in dados:
            return {'erro': 400, 'msg': 'Parametros incompletos'}
        
        vagaIdent = dados['id']
        estadoEvento = dados['estado']
        session = Session()
        try:
            vaga = session.query(Vaga).filter(Vaga.identificador == vagaIdent).first()
            if vaga is None:
                return {'erro': 404, 'msg': 'Vaga nao encontrada'}

            evento = Evento(estadoEvento, vaga.id)
            vaga.setaEstado(estadoEvento)
            # vaga.setaEvento(evento)

            session.add(evento)
            session.commit()

        except Exception as e:
            print(str(e))
            return {'erro': 500, 'msg': 'Erro ao adicionar evento'}
        finally:
            session.close()
        
        return {'msg': 'Evento adicionado'}

servicoVaga = ServicoVaga()